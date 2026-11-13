"""Structured logs, counters, and one alert rule (Day 21)."""
import json
import logging
from collections import Counter


def log_event(logger, event, **fields):
    """Log one event as a single JSON line, so tools can search it by field."""
    logger.info(json.dumps({"event": event, **fields}, sort_keys=True))


class Metrics:
    """In-process counters. A real deployment would export these."""

    def __init__(self):
        self.outcomes = Counter()
        self.reasons = Counter()
        self.durations_ms = []

    def record(self, result, duration_ms):
        self.outcomes[result.outcome.value] += 1
        if result.reason:
            self.reasons[result.reason.value] += 1
        self.durations_ms.append(duration_ms)

    @property
    def total(self):
        return sum(self.outcomes.values())

    @property
    def review_rate(self):
        return self.outcomes["needs_review"] / self.total if self.total else 0.0


def review_rate_alert(metrics, threshold=0.30, minimum_results=20):
    """Return an alert message when too many results need a person, else None.

    The minimum avoids alerting on a handful of unlucky results.
    """
    if metrics.total < minimum_results or metrics.review_rate <= threshold:
        return None
    return (
        f"review rate {metrics.review_rate:.0%} is above {threshold:.0%} "
        f"over {metrics.total} results; top reasons: {dict(metrics.reasons.most_common(3))}"
    )
