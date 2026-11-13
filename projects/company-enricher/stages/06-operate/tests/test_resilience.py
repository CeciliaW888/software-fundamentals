"""Day 24: expected failures get designed answers."""
from datetime import datetime, timezone

import pytest
from conftest import company

from enricher.adapters.resilience import RetryingWebsiteSource, retry_with_backoff
from enricher.adapters.sqlite_store import SqliteResultStore
from enricher.adapters.website import SampleWebsiteSource
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher
from enricher.core.model import Outcome, ReviewReason
from enricher.core.ports import SourceDown, TemporaryWebsiteError, WebsiteUnavailable


class FlakySource(SampleWebsiteSource):
    """Fails with a temporary error a given number of times, then answers."""

    def __init__(self, failures):
        super().__init__()
        self.failures_left = failures
        self.calls = 0

    def about_page(self, company_name):
        self.calls += 1
        if self.failures_left > 0:
            self.failures_left -= 1
            raise TemporaryWebsiteError("no answer")
        return super().about_page(company_name)


def no_sleep(seconds):
    pass


def test_a_temporary_failure_is_retried_and_then_succeeds():
    source = FlakySource(failures=2)
    page = RetryingWebsiteSource(source, attempts=3, sleep=no_sleep).about_page("Saltwater Kitchen")
    assert page.url == "https://saltwaterkitchen.example"
    assert source.calls == 3


def test_backoff_waits_longer_each_time():
    waits = []
    source = FlakySource(failures=5)
    with pytest.raises(SourceDown):
        retry_with_backoff(lambda: source.about_page("Saltwater Kitchen"), attempts=3, base_delay_seconds=0.1, sleep=waits.append)
    assert waits == [0.1, 0.2]


def test_a_permanent_failure_is_not_retried():
    source = FlakySource(failures=0)
    with pytest.raises(WebsiteUnavailable):
        RetryingWebsiteSource(source, sleep=no_sleep).about_page("Ghost Gum Traders")
    assert source.calls == 1


def test_degraded_mode_sends_companies_to_review_instead_of_stopping():
    source = RetryingWebsiteSource(FlakySource(failures=100), attempts=3, sleep=no_sleep)
    enricher = Enricher(source, KeywordCategoryClassifier(), SqliteResultStore())

    result = enricher.enrich(company("Saltwater Kitchen"))

    assert (result.outcome, result.reason) == (Outcome.NEEDS_REVIEW, ReviewReason.SOURCE_DOWN)


def test_a_retried_run_records_each_result_once():
    store = SqliteResultStore()
    fixed = datetime(2026, 1, 5, 9, 0, tzinfo=timezone.utc)
    for _attempt in range(2):  # the whole run is retried after a crash
        enricher = Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), store, clock=lambda: fixed, run_id="run-2026-01-05")
        enricher.enrich(company("Saltwater Kitchen"))

    assert len(store.history("test:Saltwater Kitchen")) == 1
