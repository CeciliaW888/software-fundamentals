"""Characterization test: every refactoring in Module 3 keeps these decisions."""
import pytest

from enricher.enricher import ACCEPTED

DECISIONS = {
    "Lantern Lane Bakery": None,
    "Bluegum Hardware": "Retail",
    "Copperleaf Software": "Software & IT",
    "Harbour Street Dental": "Healthcare",
    "Ironbark Fabrication": "Manufacturing",
    "Saltwater Kitchen": "Food & Hospitality",
    "Northgate Builders": "Construction",
    "Wattle Grove Lending": "Finance",
    "Riverbend Tutoring": "Education",
    "Paperbark Supply Co": "Wholesale & Distribution",
    "Quiet Hours Studio": None,
    "Ghost Gum Traders": None,
}


@pytest.mark.parametrize("company, category", DECISIONS.items())
def test_decision_is_unchanged(enricher, company, category):
    result = enricher.enrich(company)
    assert (result.suggestion.category if result.status == ACCEPTED else None) == category
