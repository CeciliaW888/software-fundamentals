from datetime import datetime, timezone

import pytest

from enricher.classifier import KeywordCategoryClassifier
from enricher.enricher import Enricher
from enricher.store import InMemoryResultStore
from enricher.website import SampleWebsiteSource

FIXED_TIME = datetime(2026, 1, 5, 9, 30, tzinfo=timezone.utc)


@pytest.fixture
def store():
    return InMemoryResultStore()


@pytest.fixture
def enricher(store):
    return Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), store, clock=lambda: FIXED_TIME)
