# Day 21: Observe promises and failures

[← Previous: Day 20 Protect invariants under concurrency](../week-03/day-20-invariants-under-concurrency.md) | [Course Home](../README.md) | [Next: Day 22 Deploy reversibly →](./day-22-deploy-reversibly.md)

> 📍 **Where we are in the story:** Week 4 · The service is almost ready for production. Now you run it, watch it, and recover when it fails.

---

> **Book coverage:** Observability is not covered in the three books' freely available material.
> This lesson relies on the official Python, OpenTelemetry, and OWASP documentation only.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Decide what to observe from the promises users rely on.
2. Write structured log events that tools can search by field.
3. Count outcomes and reasons as metrics.
4. Write one alert rule that fires on a real problem, not on noise.

**Plain idea:** once the service runs without you watching, its logs and numbers are how you find out whether it keeps its promises.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 6 · Operate what you build (lesson 0021)

---

## 📚 Core Concepts

### Observe: the batch ran overnight. Did it work?

The Company Enricher now runs as a nightly batch.
In the morning, the review team says the queue looks "really long today".
Is something broken?
With the Module 5 code there is no way to tell: no record of how many companies were processed, how many went to review, or why.

Start from the promises, not from the code.
What do the people who depend on the service care about?

| Promise | What would show it is broken |
|---|---|
| Most companies are categorised without a person | the share needing review jumps |
| Weak evidence goes to review, not to a wrong category | precision drops (Day 16 measures this offline) |
| A missing website does not stop the batch | many `no_website` reasons at once |
| Each company is processed in reasonable time | per-company duration grows |

### Say it plainly: events, counts, and one alarm

Stage 06 adds three things.

**A structured event per company.** After every enrichment the service logs one JSON line with named fields: the event name, a trace ID, the company ID, the outcome, the reason, and the category.
Because it is JSON, a tool can answer "show every `no_website` from last night" without parsing sentences.
The **trace ID** is a random identifier for that one enrichment, so every line about it can be found together.

**Counters.** `Metrics` counts outcomes and reasons and records each duration.
From those, the review rate is one division.

**One alert.** `review_rate_alert` returns a message when more than 30% of results need review, the Day 16 target, but only after at least 20 results, so three unlucky companies at the start of a run do not wake anyone.
The message includes the top reasons, so whoever reads it starts with a clue.

What not to log matters too.
Log company IDs, outcomes, and reasons, not whole About pages or anything personal.
OWASP's logging guidance warns against recording sensitive data in logs.

### Name it: logs, metrics, traces

OpenTelemetry, a widely used open standard for this work, describes three main **signals**:
**logs** are timestamped records of events, **metrics** are measurements aggregated over time, and **traces** follow one request through a system.
This project keeps all three small and in-process: JSON log lines through Python's `logging` module, counters in a `Metrics` object, and a trace ID on each event.
OpenTelemetry's own libraries are the next step when the service has more than one process.

**Structured logging** means writing events as fields rather than free text.
An **alert** is a rule that tells a person when an indicator crosses a threshold.

None of the three books' freely available material covers logging, metrics, or alerting, so this lesson relies on official documentation only.

> **Key Insight:** Observe the promises users depend on. Every log field and counter should help answer "is it keeping them, and if not, why?".

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Observability** | How well you can understand what a running system is doing from the data it produces. | Paraphrased from [OpenTelemetry: Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) |
| **Log** | A timestamped record of an event. | Paraphrased from [OpenTelemetry: Signals](https://opentelemetry.io/docs/concepts/signals/) |
| **Metric** | A measurement captured and aggregated over time, such as a count of outcomes. | Paraphrased from [OpenTelemetry: Signals](https://opentelemetry.io/docs/concepts/signals/) |
| **Trace ID** | An identifier shared by every record about one request, so they can be found together. | Standard observability vocabulary; this plain definition is course-authored |
| **Structured logging** | Writing log events as named fields, such as JSON, instead of free text. | Standard software vocabulary; this plain definition is course-authored |
| **Alert** | A rule that notifies a person when an indicator crosses a threshold. | Standard operations vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: One event, one JSON line

*File: [`projects/company-enricher/stages/06-operate/enricher/observability.py`](../projects/company-enricher/stages/06-operate/enricher/observability.py)*

```python
def log_event(logger, event, **fields):
    """Log one event as a single JSON line, so tools can search it by field."""
    logger.info(json.dumps({"event": event, **fields}, sort_keys=True))
```

### Example 2: What the service records after each company

*File: [`projects/company-enricher/stages/06-operate/enricher/core/enrich.py`](../projects/company-enricher/stages/06-operate/enricher/core/enrich.py)*

```python
self.metrics.record(result, duration_ms=(time.perf_counter() - started) * 1000)
log_event(
    logger,
    "enrichment_finished",
    trace_id=trace_id,
    company_id=company.company_id,
    outcome=result.outcome.value,
    reason=result.reason.value if result.reason else None,
    category=result.suggestion.category.value if result.suggestion else None,
)
```

**What's happening:** every enrichment produces one counter update and one event, with exactly the fields the promise table needs.

### Example 3: An alert that ignores noise

*File: [`projects/company-enricher/stages/06-operate/enricher/observability.py`](../projects/company-enricher/stages/06-operate/enricher/observability.py)*

```python
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
```

### Example 4: Testing what gets logged

*File: [`projects/company-enricher/stages/06-operate/tests/test_observability.py`](../projects/company-enricher/stages/06-operate/tests/test_observability.py)*

```python
def test_each_enrichment_logs_one_json_line(enricher, caplog):
    with caplog.at_level(logging.INFO, logger="enricher"):
        enricher.enrich(company("Lantern Lane Bakery"))

    event = json.loads(caplog.records[-1].getMessage())
    assert event["event"] == "enrichment_finished"
    assert event["outcome"] == "needs_review"
    assert event["reason"] == "weak_evidence"
    assert len(event["trace_id"]) == 32
```

> **💡 Try it:** in `stages/06-operate`, run `ENRICHER_DB_PATH=:memory: python -m enricher` and read the JSON lines it prints.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why log JSON fields instead of a sentence like "Lantern Lane Bakery needs review"?**

- A. JSON is shorter.
- B. Python cannot log sentences.
- C. Tools can filter and count by field without parsing text.
- D. Sentences are less accurate.

<details>
<summary>Answer</summary>

**C.** Structured fields make questions like "how many no_website reasons last night?" a simple filter.

</details>

**Q2. Why does the alert wait for at least 20 results?**

- A. To save memory
- B. Because the classifier needs warming up
- C. Python requires it
- D. So a few unlucky companies at the start do not raise a false alarm

<details>
<summary>Answer</summary>

**D.** Small samples are noisy. Alerts that fire on noise get ignored, which defeats them.

</details>

**Q3. Which field should NOT go into the enrichment log event?**

- A. The full About-page text
- B. The outcome
- C. The review reason
- D. The trace ID

<details>
<summary>Answer</summary>

**A.** Logs are copied widely and kept long. Log identifiers and outcomes; keep page content in the store, where access is controlled.

</details>

### Exercise 2 · Change: a second alert (⏱️ ~20 min)

**Goal:** Turn another promise into an alert.

**Instructions:**
1. Promise: "a missing website does not stop the batch" holds, but many `no_website` results at once usually means the website source is broken.
2. Write `no_website_alert(metrics, threshold=0.5, minimum_results=10)` in `observability.py`.
3. Write two tests: one where it fires, one where it stays quiet.
4. Call it from `__main__.py` next to the review-rate alert.

<details>
<summary>Hint</summary>

`metrics.reasons["no_website"] / metrics.total` is the share. Reuse the shape of `review_rate_alert`.

</details>

### Exercise 3 · Transfer: from promise to signal (⏱️ ~10 min)

Pick a service you rely on.
Write two promises it makes to you, and for each, the log field or metric that would show it breaking.

---

## 📖 Curated Resources

1. **[OpenTelemetry: Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)** and **[Signals](https://opentelemetry.io/docs/concepts/signals/)**
   - Why: logs, metrics, and traces explained by the standard's authors.
2. **[Python documentation: logging](https://docs.python.org/3/library/logging.html)**
   - Why: loggers, levels, and handlers used by `log_event`.
3. **[pytest: how to manage logging](https://docs.pytest.org/en/stable/how-to/logging.html)**
   - Why: the `caplog` fixture in Example 4.
4. **[OWASP: Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)**
   - Why: what not to log, and why.
5. **Book coverage:** none in the three books' freely available material; official documentation only.
   - Why: a book source should be chosen when the full books are available.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is the difference between a log and a metric?
2. **Application:** The review team says the queue is long. Which log query would you run first?
3. **Connection:** How does Day 16's review-rate target become today's alert threshold?
4. **Critical Thinking:** What could make the service look healthy in its metrics while it is actually wrong?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 22: Deploy reversibly](./day-22-deploy-reversibly.md). You can see problems now; next you make sure any change can be undone quickly.

**Before moving on, make sure you can:**

- [ ] Choose log fields from the service's promises.
- [ ] Count outcomes and compute a rate.
- [ ] Write an alert that avoids noise.

[← Previous: Day 20 Protect invariants under concurrency](../week-03/day-20-invariants-under-concurrency.md) | [Course Home](../README.md) | [Next: Day 22 Deploy reversibly →](./day-22-deploy-reversibly.md)
