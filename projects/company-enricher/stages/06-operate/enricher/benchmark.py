"""Measure before optimizing (Day 23).

    python -m enricher.benchmark            # timings per step
    python -m enricher.benchmark --profile  # cProfile, top functions

The sample source answers instantly, so this benchmark adds a fixed delay
to stand in for a real website. Change it to see how the result moves.
"""
import cProfile
import pstats
import sys
import time

from enricher.adapters.caching import CachingWebsiteSource
from enricher.adapters.sample_web import SAMPLE_WEB
from enricher.adapters.store import InMemoryResultStore
from enricher.adapters.website import SampleWebsiteSource
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher
from enricher.core.model import Company

SIMULATED_WEBSITE_DELAY_SECONDS = 0.02


class SlowSampleSource(SampleWebsiteSource):
    def about_page(self, company_name):
        time.sleep(SIMULATED_WEBSITE_DELAY_SECONDS)
        return super().about_page(company_name)


def batch(repeats=3):
    """A realistic batch: every sample company, each appearing several times."""
    return [Company(f"sample:{name}", name) for name in SAMPLE_WEB for _ in range(repeats)]


def time_steps(companies):
    source, classifier = SlowSampleSource(), KeywordCategoryClassifier()
    totals = {"read website": 0.0, "classify": 0.0}
    for company in companies:
        started = time.perf_counter()
        page = source.about_page(company.name)
        totals["read website"] += time.perf_counter() - started
        started = time.perf_counter()
        classifier.suggest(page.main_activity)
        totals["classify"] += time.perf_counter() - started
    return totals


def time_batch(source, companies):
    enricher = Enricher(source, KeywordCategoryClassifier(), InMemoryResultStore())
    started = time.perf_counter()
    for company in companies:
        enricher.enrich(company)
    return time.perf_counter() - started


def main():
    companies = batch()
    if "--profile" in sys.argv:
        profiler = cProfile.Profile()
        profiler.runcall(time_batch, SlowSampleSource(), companies)
        pstats.Stats(profiler).sort_stats("cumulative").print_stats(8)
        return
    for step, seconds in time_steps(companies).items():
        print(f"{step:14} {seconds * 1000:8.1f} ms")
    print(f"{'batch':14} {time_batch(SlowSampleSource(), companies) * 1000:8.1f} ms  without cache")
    print(f"{'batch':14} {time_batch(CachingWebsiteSource(SlowSampleSource()), companies) * 1000:8.1f} ms  with cache")


if __name__ == "__main__":
    main()
