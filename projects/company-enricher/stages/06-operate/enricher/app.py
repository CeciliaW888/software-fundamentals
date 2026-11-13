"""Build the service from settings: the one place that wires adapters (Day 22)."""
from enricher.adapters.caching import CachingWebsiteSource
from enricher.adapters.resilience import RetryingWebsiteSource
from enricher.adapters.sqlite_store import SqliteResultStore
from enricher.adapters.website import HttpWebsiteSource, SampleWebsiteSource
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher, new_run_id
from enricher.core.policy import SuggestionPolicy


def build_enricher(settings, about_urls=None):
    if settings.use_http_source:
        source = HttpWebsiteSource(about_urls or {})
    else:
        source = SampleWebsiteSource()
    source = CachingWebsiteSource(RetryingWebsiteSource(source, attempts=settings.retry_attempts))
    return Enricher(
        source,
        KeywordCategoryClassifier(),
        SqliteResultStore(settings.database_path),
        policy=SuggestionPolicy(settings.minimum_confidence),
        run_id=new_run_id(),
    )
