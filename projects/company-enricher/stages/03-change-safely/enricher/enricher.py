"""The service's one public operation: enrich a company."""
from dataclasses import dataclass
from datetime import datetime, timezone

from enricher.categories import MINIMUM_CONFIDENCE
from enricher.classifier import CategorySuggestion
from enricher.website import WebsiteUnavailable

ACCEPTED = "accepted"
NEEDS_REVIEW = "needs_review"

WEAK_EVIDENCE = "weak_evidence"
NO_WEBSITE = "no_website"


@dataclass(frozen=True)
class EnrichmentResult:
    company_name: str
    status: str
    reason: str | None
    suggestion: CategorySuggestion | None
    evidence_url: str | None
    evidence_text: str | None
    checked_at: datetime


def utc_now():
    return datetime.now(timezone.utc)


class Enricher:
    def __init__(self, websites, classifier, store, minimum_confidence=MINIMUM_CONFIDENCE, clock=utc_now):
        self._websites = websites
        self._classifier = classifier
        self._store = store
        self._minimum_confidence = minimum_confidence
        self._clock = clock

    def enrich(self, company_name):
        """Suggest a category for one company, with its evidence.

        Always returns an EnrichmentResult and never raises for an
        expected business case:
        - "accepted": confidence reached the minimum; the result is saved.
        - "needs_review", reason "weak_evidence": a suggestion exists but
          is not confident enough; nothing is saved.
        - "needs_review", reason "no_website": no About page could be read.
        """
        try:
            page = self._websites.about_page(company_name)
        except WebsiteUnavailable:
            return self._needs_review(company_name, NO_WEBSITE)

        suggestion = self._classifier.suggest(page.main_activity)
        check_confidence(suggestion.confidence)
        status = self._decide(suggestion)
        result = EnrichmentResult(
            company_name=company_name,
            status=status,
            reason=None if status == ACCEPTED else WEAK_EVIDENCE,
            suggestion=suggestion,
            evidence_url=page.url,
            evidence_text=page.main_activity,
            checked_at=self._clock(),
        )
        if result.status == ACCEPTED:
            self._store.save(result)
        return result

    def _decide(self, suggestion):
        if suggestion.confidence >= self._minimum_confidence:
            return ACCEPTED
        return NEEDS_REVIEW

    def _needs_review(self, company_name, reason):
        return EnrichmentResult(
            company_name=company_name,
            status=NEEDS_REVIEW,
            reason=reason,
            suggestion=None,
            evidence_url=None,
            evidence_text=None,
            checked_at=self._clock(),
        )


def check_confidence(confidence):
    """A confidence outside 0..1 is a bug in a classifier: stop at once."""
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"confidence must be between 0 and 1, got {confidence!r}")
