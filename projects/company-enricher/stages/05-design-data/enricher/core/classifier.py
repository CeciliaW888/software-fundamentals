"""Suggest a category for a piece of business text."""
import re

from enricher.core.categories import CATEGORY_KEYWORDS, Category
from enricher.core.model import CategorySuggestion, Confidence


class KeywordCategoryClassifier:
    """Suggests the category whose keywords appear most often."""

    def suggest(self, text):
        words = re.findall(r"[a-z]+", text.lower())
        hits = {
            category: sum(1 for word in words if word in keywords)
            for category, keywords in CATEGORY_KEYWORDS.items()
        }
        total_hits = sum(hits.values())
        if total_hits == 0:
            return CategorySuggestion(Category.OTHER, Confidence(0.0))
        best = max(hits, key=hits.get)
        return CategorySuggestion(best, Confidence(hits[best] / total_hits))
