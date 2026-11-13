"""The service's one public operation: enrich a company."""
import logging
import time
import uuid
from datetime import datetime, timezone

from enricher.core.model import EnrichmentResult, Evidence, Outcome, ReviewReason
from enricher.core.policy import SuggestionPolicy
from enricher.core.ports import SourceDown, WebsiteUnavailable
from enricher.observability import Metrics, log_event

logger = logging.getLogger("enricher")


def utc_now():
    return datetime.now(timezone.utc)


class Enricher:
    def __init__(self, websites, classifier, store, policy=None, clock=utc_now, metrics=None, run_id=None):
        self._websites = websites
        self._classifier = classifier
        self._store = store
        self._policy = policy or SuggestionPolicy()
        self._clock = clock
        self.metrics = metrics or Metrics()
        self._run_id = run_id

    def enrich(self, company):
        """Suggest a category for one company, with its evidence.

        Always returns an EnrichmentResult and records it. When the website
        source is down, the result NEEDS_REVIEW with reason SOURCE_DOWN:
        the service degrades instead of stopping.
        """
        trace_id = uuid.uuid4().hex
        started = time.perf_counter()
        result = self._enrich(company)
        self._store.save(result)
        self.metrics.record(result, duration_ms=(time.perf_counter() - started) * 1000)
        log_event(
            logger,
            "enrichment_finished",
            trace_id=trace_id,
            company_id=company.company_id,
            outcome=result.outcome.value,
            reason=result.reason.value if result.reason else None,
            category=result.suggestion.category.value if result.suggestion else None,
        )
        return result

    def _enrich(self, company):
        try:
            page = self._websites.about_page(company.name)
        except WebsiteUnavailable:
            return self._needs_review(company, ReviewReason.NO_WEBSITE)
        except SourceDown:
            return self._needs_review(company, ReviewReason.SOURCE_DOWN)

        suggestion = self._classifier.suggest(page.main_activity)
        outcome, reason = self._policy.decide(suggestion, company)
        return EnrichmentResult(
            company=company,
            outcome=outcome,
            reason=reason,
            suggestion=suggestion,
            evidence=Evidence(source_url=page.url, excerpt=page.main_activity),
            checked_at=self._clock(),
            run_id=self._run_id,
        )

    def _needs_review(self, company, reason):
        return EnrichmentResult(company, Outcome.NEEDS_REVIEW, reason, None, None, self._clock(), self._run_id)


def new_run_id():
    return uuid.uuid4().hex
