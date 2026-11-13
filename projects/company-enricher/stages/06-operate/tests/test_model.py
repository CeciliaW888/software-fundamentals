import pytest

from enricher.core.categories import Category
from enricher.core.model import CategorySuggestion, Company, Confidence


def test_confidence_rejects_impossible_values():
    with pytest.raises(ValueError):
        Confidence(1.7)


def test_value_objects_are_equal_by_value():
    assert CategorySuggestion(Category.FOOD, Confidence(0.9)) == CategorySuggestion(Category.FOOD, Confidence(0.9))


def test_company_keeps_its_identity_when_renamed():
    before = Company(company_id="tradeline:TL-0042", name="Saltwater Kitchen")
    after = Company(company_id="tradeline:TL-0042", name="Saltwater Kitchen & Bar")
    assert before == after
    assert Company("a", "Same Name") != Company("b", "Same Name")
