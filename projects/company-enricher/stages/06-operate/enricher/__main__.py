"""Run one batch over the sample companies: python -m enricher

Settings come from ENRICHER_* environment variables (see settings.py).
"""
import logging

from enricher.adapters.sample_web import SAMPLE_WEB
from enricher.app import build_enricher
from enricher.core.model import Company
from enricher.observability import review_rate_alert
from enricher.settings import Settings

logging.basicConfig(level=logging.INFO, format="%(message)s")
enricher = build_enricher(Settings.from_env())
for number, name in enumerate([*SAMPLE_WEB, "Ghost Gum Traders"], start=1):
    enricher.enrich(Company(company_id=f"sample:{number}", name=name))
alert = review_rate_alert(enricher.metrics, minimum_results=10)
if alert:
    logging.getLogger("enricher").warning(alert)
