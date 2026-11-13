"""The service's one public operation: enrich a company."""
from datetime import datetime, timezone

from enricher.core.model import EnrichmentResult, Evidence, Outcome, ReviewReason
from enricher.core.policy import SuggestionPolicy
from enricher.core.ports import WebsiteUnavailable


def utc_now():
    return datetime.now(timezone.utc)


class Enricher:
    def __init__(self, websites, classifier, store, policy=None, clock=utc_now):
        self._websites = websites
        self._classifier = classifier
        self._store = store
        self._policy = policy or SuggestionPolicy()
        self._clock = clock

    def enrich(self, company):
        """Suggest a category for one company, with its evidence.

        Always returns an EnrichmentResult. A SUGGESTED result is saved.
        A result that NEEDS_REVIEW carries the reason and is not saved.
        """
        try:
            page = self._websites.about_page(company.name)
        except WebsiteUnavailable:
            return EnrichmentResult(company, Outcome.NEEDS_REVIEW, ReviewReason.NO_WEBSITE, None, None, self._clock())

        suggestion = self._classifier.suggest(page.main_activity)
        outcome, reason = self._policy.decide(suggestion, company)
        result = EnrichmentResult(
            company=company,
            outcome=outcome,
            reason=reason,
            suggestion=suggestion,
            evidence=Evidence(source_url=page.url, excerpt=page.main_activity),
            checked_at=self._clock(),
        )
        if outcome is Outcome.SUGGESTED:
            self._store.save(result)
        return result
