"""Day 11 exercise: Enricher.enrich before the refactoring.

It works and the tests pass, but the decision is computed twice.
Refactor it under the characterization tests without changing behaviour.
"""
from enricher.enricher import ACCEPTED, WEAK_EVIDENCE, EnrichmentResult, check_confidence
from enricher.website import WebsiteUnavailable
from enricher.enricher import NO_WEBSITE


class EnricherBeforeRefactor:
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
        result = EnrichmentResult(
            company_name=company_name,
            status=self._decide(suggestion),
            reason=None if self._decide(suggestion) == ACCEPTED else WEAK_EVIDENCE,
            suggestion=suggestion,
            evidence_url=page.url,
            evidence_text=page.main_activity,
            checked_at=self._clock(),
        )
        if result.status == ACCEPTED:
            self._store.save(result)
        return result

