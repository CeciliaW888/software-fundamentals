"""Measurable quality targets for the Company Enricher (Day 16).

The targets are the team's own choices for this practice service.
"""
import math
import time
from dataclasses import dataclass

from enricher.core.categories import Category
from enricher.core.model import Company, Outcome

QUALITY_TARGETS = {
    "minimum_precision": 0.95,  # of SUGGESTED results, the share that are right
    "maximum_review_rate": 0.30,  # share of companies sent to a person
    "maximum_p95_latency_ms": 50.0,  # per company, with the sample website source
}

# What a person decided for each sample company. None means "a person must look".
LABELLED_SAMPLE = {
    "Lantern Lane Bakery": None,
    "Bluegum Hardware": Category.RETAIL,
    "Copperleaf Software": Category.SOFTWARE,
    "Harbour Street Dental": Category.HEALTHCARE,
    "Ironbark Fabrication": Category.MANUFACTURING,
    "Saltwater Kitchen": Category.FOOD,
    "Northgate Builders": Category.CONSTRUCTION,
    "Wattle Grove Lending": Category.FINANCE,
    "Riverbend Tutoring": Category.EDUCATION,
    "Paperbark Supply Co": Category.WHOLESALE,
    "Quiet Hours Studio": None,
    "Ghost Gum Traders": None,
}


@dataclass(frozen=True)
class QualityReport:
    precision: float
    review_rate: float
    p95_latency_ms: float

    def meets(self, targets=QUALITY_TARGETS):
        return (
            self.precision >= targets["minimum_precision"]
            and self.review_rate <= targets["maximum_review_rate"]
            and self.p95_latency_ms <= targets["maximum_p95_latency_ms"]
        )


def measure(enricher, labelled=LABELLED_SAMPLE):
    latencies_ms, suggested, correct, reviewed = [], 0, 0, 0
    for number, (name, expected) in enumerate(labelled.items(), start=1):
        started = time.perf_counter()
        result = enricher.enrich(Company(company_id=f"sample:{number}", name=name))
        latencies_ms.append((time.perf_counter() - started) * 1000)
        if result.outcome is Outcome.SUGGESTED:
            suggested += 1
            correct += result.suggestion.category is expected
        else:
            reviewed += 1
    latencies_ms.sort()
    p95 = latencies_ms[math.ceil(0.95 * len(latencies_ms)) - 1]
    return QualityReport(
        precision=correct / suggested if suggested else 1.0,
        review_rate=reviewed / len(labelled),
        p95_latency_ms=p95,
    )
