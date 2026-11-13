"""Day 6: the short-function version and the deep version give the same answers."""
import pytest

from enricher.classifier import KeywordCategoryClassifier
from enricher.sample_web import SAMPLE_WEB
from exercises.day06_short_functions import suggest_category


@pytest.mark.parametrize("about", [page["about"] for page in SAMPLE_WEB.values()])
def test_both_designs_suggest_the_same_category(about):
    deep = KeywordCategoryClassifier().suggest(about)
    assert suggest_category(about) == (deep.category, deep.confidence)
