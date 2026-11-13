"""Property-style tests: rules that must hold for any input, not just examples."""
import random

import pytest

from enricher.categories import CATEGORIES, CATEGORY_KEYWORDS
from enricher.classifier import KeywordCategoryClassifier
from enricher.enricher import check_confidence

VOCABULARY = sorted({word for words in CATEGORY_KEYWORDS.values() for word in words} | {"the", "and", "we", "our"})


@pytest.mark.parametrize("seed", range(200))
def test_any_text_gets_a_known_category_and_a_confidence_between_0_and_1(seed):
    rng = random.Random(seed)
    text = " ".join(rng.choice(VOCABULARY) for _ in range(rng.randint(0, 12)))

    suggestion = KeywordCategoryClassifier().suggest(text)

    assert suggestion.category in CATEGORIES
    assert 0.0 <= suggestion.confidence <= 1.0


def test_impossible_confidence_stops_the_program():
    with pytest.raises(ValueError):
        check_confidence(1.7)
