"""Tracer bullet: run the whole service end to end on the sample companies.

    python -m enricher
"""
from enricher.classifier import KeywordCategoryClassifier
from enricher.enricher import Enricher
from enricher.sample_web import SAMPLE_WEB
from enricher.store import InMemoryResultStore
from enricher.website import SampleWebsiteSource

enricher = Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), InMemoryResultStore())
for company_name in [*SAMPLE_WEB, "Ghost Gum Traders"]:
    result = enricher.enrich(company_name)
    print(f"{company_name:22} {result.status:13} {result.reason or ''}")
