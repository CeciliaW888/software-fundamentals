from datetime import datetime, timedelta, timezone

import pytest
from conftest import company

from enricher.adapters.sqlite_store import AlreadyConfirmed, SqliteResultStore
from enricher.adapters.website import SampleWebsiteSource
from enricher.core.categories import Category
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher

START = datetime(2026, 1, 5, 9, 0, tzinfo=timezone.utc)


@pytest.fixture
def sqlite_store():
    return SqliteResultStore()


def enrich_in_order(store, names):
    times = iter(START + timedelta(minutes=minute) for minute in range(100))
    enricher = Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), store, clock=lambda: next(times))
    return [enricher.enrich(company(name)) for name in names]


def test_review_queue_lists_waiting_results_oldest_first(sqlite_store):
    enrich_in_order(sqlite_store, ["Quiet Hours Studio", "Saltwater Kitchen", "Lantern Lane Bakery"])

    queue = sqlite_store.review_queue()

    assert [row["company_id"] for row in queue] == ["test:Quiet Hours Studio", "test:Lantern Lane Bakery"]


def test_latest_result_and_history(sqlite_store):
    enrich_in_order(sqlite_store, ["Saltwater Kitchen", "Saltwater Kitchen"])

    history = sqlite_store.history("test:Saltwater Kitchen")

    assert len(history) == 2
    assert sqlite_store.latest_result("test:Saltwater Kitchen")["result_id"] == history[-1]["result_id"]


def test_new_rows_record_the_classifier_version(sqlite_store):
    enrich_in_order(sqlite_store, ["Saltwater Kitchen"])
    assert sqlite_store.latest_result("test:Saltwater Kitchen")["classifier_version"] == "keywords-1"


def test_second_confirmation_for_a_company_is_refused(sqlite_store):
    enrich_in_order(sqlite_store, ["Lantern Lane Bakery"])
    sqlite_store.confirm_category("test:Lantern Lane Bakery", Category.FOOD, "reviewer-a", START)

    with pytest.raises(AlreadyConfirmed):
        sqlite_store.confirm_category("test:Lantern Lane Bakery", Category.MANUFACTURING, "reviewer-b", START)
