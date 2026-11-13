"""Day 6 comparison: the classifier split into many short functions.

Every function is short, but knowledge about categories and hit counts
is spread across all of them, and callers must call them in the right
order. Compare with KeywordCategoryClassifier.suggest in classifier.py.
"""
import re

from enricher.categories import CATEGORY_KEYWORDS, OTHER


def tokenize(text):
    return re.findall(r"[a-z]+", text.lower())


def count_hits(words):
    return {category: sum(1 for word in words if word in keywords) for category, keywords in CATEGORY_KEYWORDS.items()}


def total_hits(hits):
    return sum(hits.values())


def best_category(hits):
    return max(hits, key=hits.get)


def confidence_for(hits, category):
    return hits[category] / total_hits(hits)


def suggest_category(text):
    hits = count_hits(tokenize(text))
    if total_hits(hits) == 0:
        return OTHER, 0.0
    category = best_category(hits)
    return category, confidence_for(hits, category)
