"""Tracer bullet: python -m enricher"""
from enricher.adapters.sample_web import SAMPLE_WEB
from enricher.adapters.store import InMemoryResultStore
from enricher.adapters.website import SampleWebsiteSource
from enricher.core.classifier import KeywordCategoryClassifier
from enricher.core.enrich import Enricher
from enricher.core.model import Company

enricher = Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), InMemoryResultStore())
for number, name in enumerate([*SAMPLE_WEB, "Ghost Gum Traders"], start=1):
    result = enricher.enrich(Company(company_id=f"sample:{number}", name=name))
    print(f"{name:22} {result.outcome.value:13} {result.reason.value if result.reason else ''}")
