from datetime import datetime, timezone

import pytest

from enricher.adapters.store import InMemoryResultStore
from enricher.adapters.website import SampleWebsiteSource
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher
from enricher.core.model import Company

FIXED_TIME = datetime(2026, 1, 5, 9, 30, tzinfo=timezone.utc)


def company(name, hint=None):
    return Company(company_id=f"test:{name}", name=name, directory_hint=hint)


@pytest.fixture
def store():
    return InMemoryResultStore()


@pytest.fixture
def enricher(store):
    return Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), store, clock=lambda: FIXED_TIME)
