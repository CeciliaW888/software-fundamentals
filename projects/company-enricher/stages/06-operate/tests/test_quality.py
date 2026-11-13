"""Day 16: the quality targets are tests, so a regression fails the build."""
from enricher.adapters.store import InMemoryResultStore
from enricher.adapters.website import SampleWebsiteSource
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher
from enricher.quality import QUALITY_TARGETS, measure


def test_the_service_meets_its_quality_targets():
    report = measure(Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), InMemoryResultStore()))

    assert report.precision >= QUALITY_TARGETS["minimum_precision"]
    assert report.review_rate <= QUALITY_TARGETS["maximum_review_rate"]
    assert report.p95_latency_ms <= QUALITY_TARGETS["maximum_p95_latency_ms"]
