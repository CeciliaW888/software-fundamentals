"""Tests for what other code may rely on, not for how the work is done."""
import pytest

from enricher import (
    CategorySuggestion,
    KeywordCategoryClassifier,
    SuggestionList,
    WebsiteUnavailable,
    select_confident_category_suggestions,
    suggest_company_category,
)


def classifier_returning(category, confidence):
    """A stand-in classifier that always suggests the same thing."""

    class FixedClassifier:
        def suggest(self, activity_summary):
            return CategorySuggestion(category, confidence)

    return FixedClassifier()


def recording_store():
    return SuggestionList()


def test_weak_suggestion_is_not_saved():
    classifier = classifier_returning(
        category="Manufacturing",
        confidence=0.61,
    )
    store = recording_store()

    result = suggest_company_category(
        "Lantern Lane Bakery",
        classifier,
        store,
    )

    assert result is None
    assert store.saved_suggestions == []


def test_confident_suggestion_is_saved_and_returned():
    store = recording_store()
    result = suggest_company_category("Saltwater Kitchen", classifier_returning("Food & Hospitality", 0.9), store)
    assert result == CategorySuggestion("Food & Hospitality", 0.9)
    assert store.saved_suggestions == [("Saltwater Kitchen", result)]


def test_unknown_company_raises_website_unavailable():
    with pytest.raises(WebsiteUnavailable):
        suggest_company_category("Ghost Gum Traders", KeywordCategoryClassifier(), recording_store())


def test_renamed_selector_keeps_only_confident_texts():
    texts = ["A seaside restaurant and cafe", "We help people find calm"]
    assert select_confident_category_suggestions(texts, KeywordCategoryClassifier()) == ["A seaside restaurant and cafe"]
