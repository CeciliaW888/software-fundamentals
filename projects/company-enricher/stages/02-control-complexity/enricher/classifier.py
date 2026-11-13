"""Suggest a category for a piece of business text."""
import re
from dataclasses import dataclass

from enricher.categories import CATEGORY_KEYWORDS, OTHER


@dataclass(frozen=True)
class CategorySuggestion:
    category: str
    confidence: float


class KeywordCategoryClassifier:
    """Suggests the category whose keywords appear most often.

    Confidence is the share of keyword hits that belong to the winning
    category. Text with no keywords is "Other" with confidence 0.0.
    """

    def suggest(self, text):
        words = re.findall(r"[a-z]+", text.lower())
        hits = {
            category: sum(1 for word in words if word in keywords)
            for category, keywords in CATEGORY_KEYWORDS.items()
        }
        total_hits = sum(hits.values())
        if total_hits == 0:
            return CategorySuggestion(OTHER, 0.0)
        best = max(hits, key=hits.get)
        return CategorySuggestion(best, hits[best] / total_hits)
