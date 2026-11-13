from enricher.adapters.caching import CachingWebsiteSource
from enricher.adapters.website import SampleWebsiteSource


class CountingSource(SampleWebsiteSource):
    def __init__(self):
        super().__init__()
        self.calls = 0

    def about_page(self, company_name):
        self.calls += 1
        return super().about_page(company_name)


def test_cache_reads_each_website_once_per_run():
    inner = CountingSource()
    cached = CachingWebsiteSource(inner)

    for _ in range(3):
        cached.about_page("Saltwater Kitchen")

    assert inner.calls == 1


def test_cache_returns_the_same_page():
    cached = CachingWebsiteSource(SampleWebsiteSource())
    assert cached.about_page("Bluegum Hardware") == SampleWebsiteSource().about_page("Bluegum Hardware")
