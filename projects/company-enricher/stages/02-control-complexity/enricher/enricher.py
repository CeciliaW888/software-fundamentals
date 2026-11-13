"""The service's one public operation: enrich a company."""
from dataclasses import dataclass

from enricher.categories import MINIMUM_CONFIDENCE
from enricher.classifier import CategorySuggestion

ACCEPTED = "accepted"
NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class EnrichmentResult:
    company_name: str
    status: str
    suggestion: CategorySuggestion
    evidence_url: str
    evidence_text: str


class Enricher:
    def __init__(self, websites, classifier, store, minimum_confidence=MINIMUM_CONFIDENCE):
        self._websites = websites
        self._classifier = classifier
        self._store = store
        self._minimum_confidence = minimum_confidence

    def enrich(self, company_name):
        """Suggest a category for one company, with its evidence.

        Always returns an EnrichmentResult. Its status is "accepted" when
        confidence reaches the minimum, and the result is then saved;
        otherwise it is "needs_review" and nothing is saved.
        Raises WebsiteUnavailable when no About page can be read.
        """
        page = self._websites.about_page(company_name)
        suggestion = self._classifier.suggest(page.main_activity)
        accepted = suggestion.confidence >= self._minimum_confidence
        result = EnrichmentResult(
            company_name=company_name,
            status=ACCEPTED if accepted else NEEDS_REVIEW,
            suggestion=suggestion,
            evidence_url=page.url,
            evidence_text=page.main_activity,
        )
        if accepted:
            self._store.save(result)
        return result
