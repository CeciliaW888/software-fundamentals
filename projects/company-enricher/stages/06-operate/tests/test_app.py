from enricher.adapters.website import HttpWebsiteSource, SampleWebsiteSource
from enricher.app import build_enricher
from enricher.settings import Settings


def innermost_source(enricher):
    source = enricher._websites
    while hasattr(source, "_inner"):
        source = source._inner
    return source


def test_flag_off_uses_the_sample_source():
    enricher = build_enricher(Settings(database_path=":memory:"))
    assert isinstance(innermost_source(enricher), SampleWebsiteSource)


def test_flag_on_uses_the_http_source():
    enricher = build_enricher(Settings(database_path=":memory:", use_http_source=True))
    assert isinstance(innermost_source(enricher), HttpWebsiteSource)
