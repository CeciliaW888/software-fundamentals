"""The domain model renamed things; the decisions for sample companies stay the same."""
import pytest
from conftest import company

from enricher.core.model import Outcome

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


@pytest.mark.parametrize("name, category", DECISIONS.items())
def test_decision_is_unchanged(enricher, name, category):
    result = enricher.enrich(company(name))
    assert (result.suggestion.category.value if result.outcome is Outcome.SUGGESTED else None) == category
