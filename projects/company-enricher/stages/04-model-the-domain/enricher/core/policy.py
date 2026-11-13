"""When may the service suggest a category without a person checking it?"""
from enricher.core.model import Outcome, ReviewReason

MINIMUM_CONFIDENCE = 0.82


class SuggestionPolicy:
    """A domain service: the rule involves a suggestion and a company,
    and belongs naturally to neither."""

    def __init__(self, minimum_confidence=MINIMUM_CONFIDENCE):
        self._minimum_confidence = minimum_confidence

    def decide(self, suggestion, company):
        """Return (Outcome, ReviewReason or None)."""
        if not suggestion.confidence.at_least(self._minimum_confidence):
            return Outcome.NEEDS_REVIEW, ReviewReason.WEAK_EVIDENCE
        if company.directory_hint and company.directory_hint != suggestion.category:
            return Outcome.NEEDS_REVIEW, ReviewReason.CONFLICTING_SOURCES
        return Outcome.SUGGESTED, None
