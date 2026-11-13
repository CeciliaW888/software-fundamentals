"""Module 1 changed names, not decisions: same companies, same categories."""
import pytest

from enricher import KeywordCategoryClassifier, SuggestionList, suggest_company_category

SAME_AS_INHERITED_SCRIPT = {
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
}


@pytest.mark.parametrize("company, category", SAME_AS_INHERITED_SCRIPT.items())
def test_same_category_as_the_inherited_script(company, category):
    result = suggest_company_category(company, KeywordCategoryClassifier(), SuggestionList())
    assert (result.category if result else None) == category
