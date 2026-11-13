import json
import logging

from conftest import company

from enricher.observability import Metrics, review_rate_alert


def test_each_enrichment_logs_one_json_line(enricher, caplog):
    with caplog.at_level(logging.INFO, logger="enricher"):
        enricher.enrich(company("Lantern Lane Bakery"))

    event = json.loads(caplog.records[-1].getMessage())
    assert event["event"] == "enrichment_finished"
    assert event["outcome"] == "needs_review"
    assert event["reason"] == "weak_evidence"
    assert len(event["trace_id"]) == 32


def test_metrics_count_outcomes_and_reasons(enricher):
    enricher.enrich(company("Saltwater Kitchen"))
    enricher.enrich(company("Ghost Gum Traders"))

    assert enricher.metrics.outcomes == {"suggested": 1, "needs_review": 1}
    assert enricher.metrics.reasons == {"no_website": 1}


def test_alert_fires_only_when_the_review_rate_is_high_over_enough_results(enricher):
    for _ in range(10):
        enricher.enrich(company("Saltwater Kitchen"))
        enricher.enrich(company("Quiet Hours Studio"))

    assert review_rate_alert(enricher.metrics) is not None
    assert review_rate_alert(Metrics()) is None
