"""Pin what the inherited script does today, before anyone changes it."""
import pytest

from enricher import M, go, run

EXPECTED = {
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


@pytest.mark.parametrize("company, category", EXPECTED.items())
def test_go_returns_the_same_category_as_before(company, category):
    db = []
    assert go(company, db) == category
    assert len(db) == (0 if category is None else 1)


def test_go_raises_for_an_unknown_company():
    with pytest.raises(Exception, match="no site"):
        go("Ghost Gum Traders", [])


def test_run_keeps_only_confident_texts():
    texts = ["A seaside restaurant and cafe", "We help people find calm"]
    assert run(texts, M()) == ["A seaside restaurant and cafe"]
