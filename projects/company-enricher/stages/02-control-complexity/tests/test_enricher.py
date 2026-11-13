import pytest

from enricher.classifier import KeywordCategoryClassifier
from enricher.enricher import ACCEPTED, NEEDS_REVIEW, Enricher
from enricher.store import InMemoryResultStore
from enricher.website import CompanyWebsites, WebsiteUnavailable

SAME_DECISIONS_AS_MODULE_1 = {
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


def make_enricher():
    return Enricher(CompanyWebsites(), KeywordCategoryClassifier(), InMemoryResultStore())


@pytest.mark.parametrize("company, category", SAME_DECISIONS_AS_MODULE_1.items())
def test_accepts_the_same_companies_as_module_1(company, category):
    result = make_enricher().enrich(company)
    accepted_category = result.suggestion.category if result.status == ACCEPTED else None
    assert accepted_category == category


def test_weak_evidence_needs_review_and_is_not_saved():
    store = InMemoryResultStore()
    enricher = Enricher(CompanyWebsites(), KeywordCategoryClassifier(), store)
    result = enricher.enrich("Lantern Lane Bakery")
    assert result.status == NEEDS_REVIEW
    assert result.evidence_url == "https://lanternlanebakery.example"
    assert store.saved_results == []


def test_accepted_result_is_saved_with_its_evidence():
    store = InMemoryResultStore()
    result = Enricher(CompanyWebsites(), KeywordCategoryClassifier(), store).enrich("Saltwater Kitchen")
    assert store.saved_results == [result]
    assert result.evidence_text.startswith("A seaside restaurant")


def test_unknown_company_raises_website_unavailable():
    with pytest.raises(WebsiteUnavailable):
        make_enricher().enrich("Ghost Gum Traders")


def test_adding_a_category_is_one_edit(monkeypatch):
    from enricher import categories

    monkeypatch.setitem(categories.CATEGORY_KEYWORDS, "Agriculture", {"farm", "crops"})
    suggestion = KeywordCategoryClassifier().suggest("We farm crops")
    assert suggestion.category == "Agriculture"
