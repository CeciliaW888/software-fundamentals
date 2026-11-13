"""Scenarios written with the business, in the business's words."""
import pytest
from conftest import company

from enricher.core.categories import Category
from enricher.core.model import Outcome, ReviewReason

SCENARIOS = [
    ("Saltwater Kitchen", None, Outcome.SUGGESTED, None),
    ("Lantern Lane Bakery", None, Outcome.NEEDS_REVIEW, ReviewReason.WEAK_EVIDENCE),
    ("Ghost Gum Traders", None, Outcome.NEEDS_REVIEW, ReviewReason.NO_WEBSITE),
    ("Ironbark Fabrication", Category.CONSTRUCTION, Outcome.NEEDS_REVIEW, ReviewReason.CONFLICTING_SOURCES),
    ("Ironbark Fabrication", Category.MANUFACTURING, Outcome.SUGGESTED, None),
]


@pytest.mark.parametrize("name, hint, outcome, reason", SCENARIOS)
def test_scenario(enricher, name, hint, outcome, reason):
    result = enricher.enrich(company(name, hint))
    assert (result.outcome, result.reason) == (outcome, reason)


def test_only_suggested_results_are_saved(enricher, store):
    suggested = enricher.enrich(company("Saltwater Kitchen"))
    enricher.enrich(company("Lantern Lane Bakery"))
    assert store.saved_results == [suggested]
