"""Each test checks one promise from Enricher.enrich's docstring."""
from conftest import FIXED_TIME

from enricher.enricher import ACCEPTED, NEEDS_REVIEW, NO_WEBSITE, WEAK_EVIDENCE


def test_confident_suggestion_is_accepted_and_saved(enricher, store):
    result = enricher.enrich("Saltwater Kitchen")

    assert result.status == ACCEPTED
    assert result.suggestion.category == "Food & Hospitality"
    assert store.saved_results == [result]


def test_weak_evidence_needs_review_and_is_not_saved(enricher, store):
    result = enricher.enrich("Lantern Lane Bakery")

    assert result.status == NEEDS_REVIEW
    assert result.reason == WEAK_EVIDENCE
    assert store.saved_results == []


def test_missing_website_needs_review_instead_of_crashing(enricher, store):
    result = enricher.enrich("Ghost Gum Traders")

    assert result.status == NEEDS_REVIEW
    assert result.reason == NO_WEBSITE
    assert store.saved_results == []


def test_result_records_when_it_was_checked(enricher):
    assert enricher.enrich("Bluegum Hardware").checked_at == FIXED_TIME
