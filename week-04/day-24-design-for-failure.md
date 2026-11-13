# Day 24: Design for expected failure

[← Previous: Day 23 Measure before optimizing](./day-23-measure-before-optimizing.md) | [Course Home](../README.md)

> 📍 **Where we are in the story:** Week 4 · The service is almost ready for production. Now you run it, watch it, and recover when it fails.

---

> **Book coverage:** Retries, timeouts, and idempotency are not covered in the three books' freely available material.
> Those parts rely on the official Python, SQLite, and HTTP documentation; the error-handling shape follows Ousterhout's Chapter 10, marked to verify against the book.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Tell temporary failures from permanent ones, and handle each differently.
2. Retry temporary failures with a limited number of attempts and growing waits.
3. Make a retried run safe with an idempotency key.
4. Keep the service useful in degraded mode when a dependency is down.

**Plain idea:** in production, failure is normal; decide in advance what each kind means so the service bends instead of breaking.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 45 minutes (20 reading + 25 hands-on)\
**Module:** 6 · Operate what you build (lesson 0024)

---

## 📚 Core Concepts

### Observe: three bad nights

With real websites switched on (Day 22's flag), three things happen in the first month.

1. **A website answers slowly once, then fine.** The Module 5 code treats a timeout as "no website" and sends the company to review, although one more try would have worked.
2. **The network is down for an hour.** Every company goes to review as "no website", flooding the queue with cases that need no human judgement, and Day 21's alert fires.
3. **The batch crashes halfway and is restarted.** Companies processed before the crash are processed again, and each now has two identical results in its history.

None of these is a bug in the classifier.
They are the normal behaviour of networks and processes, and the service needs a designed answer for each.

### Say it plainly: four designed answers

**Temporary or permanent?** A timeout is temporary: trying again may work. "This company has no website" is permanent: trying again will not help.
Stage 06 gives them different exceptions.
The HTTP adapter turns a `TimeoutError` into `TemporaryWebsiteError`, and keeps `WebsiteUnavailable` for permanent cases.

**Retry temporary failures, a few times, with growing waits.** `RetryingWebsiteSource` wraps any source.
On a temporary error it waits 0.2 seconds, then 0.4, and gives up after three attempts.
Growing waits give a struggling server room to recover instead of hammering it.
Permanent errors are never retried.
A timeout on each attempt (Day 10) puts a ceiling on how long one company can take.

**Degrade, don't stop.** When every retry fails, the source raises `SourceDown`.
The core turns that into a result that needs review with a new reason, `source_down`, so the run finishes, nothing is lost, and the reason tells reviewers that these cases can simply be retried later rather than judged.

**Make a repeated run harmless.** Each batch run has a run ID.
The store records each result with an idempotency key made from the run ID and the company ID, and migration 5 adds a unique index on it.
If a crashed run is restarted with the same run ID, saving the same company again does nothing.

### Name it: transient faults, backoff, idempotency, degraded mode

A **transient failure** is one that may succeed if tried again; a **permanent failure** will not.
**Exponential backoff** doubles the wait between attempts.
An operation is **idempotent** if doing it several times has the same effect as doing it once; the HTTP standard, RFC 9110, defines idempotent request methods in exactly this sense.
SQLite's `ON CONFLICT ... DO NOTHING` clause (its "upsert" syntax) is what makes the second save a no-op.
**Degraded mode** is running with reduced capability instead of stopping.

John Ousterhout's *A Philosophy of Software Design*, Chapter 10, "Define Errors Out Of Existence" (to verify against book), explains the design shape: the retrying source masks temporary failures so callers never see them, and the core aggregates every website problem into a review result.

None of the three books' freely available material covers retries, backoff, or idempotency; those parts rely on official documentation only.
Ousterhout's ideas on masking errors, from Chapter 10 (to verify against book), shape the design.

> **Key Insight:** For every dependency, decide three things in advance: what counts as temporary, how many times to retry, and what the service does when retries run out.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Transient failure** | A failure that may succeed if the same request is tried again. | Standard software vocabulary; this plain definition is course-authored |
| **Retry with backoff** | Trying a failed operation again after waits that grow each time. | Standard software vocabulary; this plain definition is course-authored |
| **Idempotent** | Having the same effect whether done once or many times. | Paraphrased from [RFC 9110, HTTP Semantics: idempotent methods](https://www.rfc-editor.org/rfc/rfc9110#name-idempotent-methods) |
| **Idempotency key** | An identifier that lets a system recognise a repeated request and apply it only once. | Standard software vocabulary; this plain definition is course-authored |
| **Upsert** | An insert that does something else, such as nothing, when the row already exists. | Official SQLite vocabulary ([UPSERT](https://www.sqlite.org/lang_upsert.html)) |
| **Degraded mode** | Running with reduced capability instead of stopping when a dependency fails. | Standard software vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: Temporary versus permanent, at the boundary

*File: [`projects/company-enricher/stages/06-operate/enricher/adapters/website.py`](../projects/company-enricher/stages/06-operate/enricher/adapters/website.py)*

```python
try:
    html = self._fetch(url, self._timeout_seconds)
except TimeoutError as error:
    raise TemporaryWebsiteError(f"{company_name}: timed out") from error
except OSError as error:
    raise WebsiteUnavailable(f"{company_name}: {error}") from error
```

**What's happening:** `TimeoutError` is a kind of `OSError`, so it must be caught first.

### Example 2: Retry with backoff

*File: [`projects/company-enricher/stages/06-operate/enricher/adapters/resilience.py`](../projects/company-enricher/stages/06-operate/enricher/adapters/resilience.py)*

```python
def retry_with_backoff(call, attempts=3, base_delay_seconds=0.2, sleep=time.sleep):
    """Run call(); after a TemporaryWebsiteError wait and try again.

    Waits base_delay, then 2 x base_delay, and so on. Any other error is
    not retried. After the last attempt, raises SourceDown.
    """
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except TemporaryWebsiteError as error:
            if attempt == attempts:
                raise SourceDown(str(error)) from error
            sleep(base_delay_seconds * 2 ** (attempt - 1))
```

**What's happening:** `sleep` is injectable, so tests check the waits without actually waiting.

### Example 3: Degraded mode in the core

*File: [`projects/company-enricher/stages/06-operate/enricher/core/enrich.py`](../projects/company-enricher/stages/06-operate/enricher/core/enrich.py)*

```python
try:
    page = self._websites.about_page(company.name)
except WebsiteUnavailable:
    return self._needs_review(company, ReviewReason.NO_WEBSITE)
except SourceDown:
    return self._needs_review(company, ReviewReason.SOURCE_DOWN)
```

### Example 4: A repeated save does nothing

*File: [`projects/company-enricher/stages/06-operate/enricher/adapters/migrations.py`](../projects/company-enricher/stages/06-operate/enricher/adapters/migrations.py)*

```sql
ALTER TABLE results ADD COLUMN idempotency_key TEXT;
CREATE UNIQUE INDEX results_idempotency_key
    ON results (idempotency_key);
```

*File: [`projects/company-enricher/stages/06-operate/tests/test_resilience.py`](../projects/company-enricher/stages/06-operate/tests/test_resilience.py)*

```python
def test_a_retried_run_records_each_result_once():
    store = SqliteResultStore()
    fixed = datetime(2026, 1, 5, 9, 0, tzinfo=timezone.utc)
    for _attempt in range(2):  # the whole run is retried after a crash
        enricher = Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), store, clock=lambda: fixed, run_id="run-2026-01-05")
        enricher.enrich(company("Saltwater Kitchen"))

    assert len(store.history("test:Saltwater Kitchen")) == 1
```

**What's happening:** two runs with the same run ID save the company once, because the second insert hits the unique key and does nothing.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which failure should be retried?**

- A. The company has no website at all
- B. The classifier returned confidence 1.7
- C. A reviewer confirmed a category twice
- D. The website timed out once

<details>
<summary>Answer</summary>

**D.** A timeout is transient. A missing website is permanent, an impossible confidence is a bug, and a double confirmation is an invariant violation.

</details>

**Q2. Why do the waits grow between retries?**

- A. To give a struggling server time to recover instead of hammering it
- B. To make the batch slower on purpose
- C. Because Python's sleep is inaccurate
- D. To use less memory

<details>
<summary>Answer</summary>

**A.** Backing off reduces load on the failing dependency and raises the chance the next attempt succeeds.

</details>

**Q3. A crashed batch is restarted with the same run ID. What stops duplicate results?**

- A. The cache from Day 23
- B. The unique index on the idempotency key
- C. The retry loop
- D. The review queue

<details>
<summary>Answer</summary>

**B.** Same run and same company give the same key, so the second insert does nothing.

</details>

### Exercise 2 · Change: a capstone failure drill (⏱️ ~25 min)

**Goal:** Prove the service survives a bad night, end to end.

**Instructions:**
1. In `stages/06-operate/tests/`, write a test that builds an `Enricher` with a source that is down for the first five companies and healthy after that.
2. Run it over every sample company plus Ghost Gum Traders.
3. Assert: the run finishes; the first five results have reason `source_down`; Ghost Gum Traders has `no_website`; the rest match `LABELLED_SAMPLE`.
4. Assert that Day 21's alert fires with `source_down` in its message.
5. Run `./run_all_tests.sh` from `projects/company-enricher`; every stage should still pass.

<details>
<summary>Hint</summary>

Reuse `FlakySource` from `test_resilience.py`, wrapped in `RetryingWebsiteSource` with `sleep=no_sleep`, and give it a counter of companies rather than of calls.

</details>

### Exercise 3 · Transfer: a failure plan for one dependency (⏱️ ~10 min)

Pick one external dependency of a system you know.
Write its failure plan in four lines: what is temporary, how many retries, how long each may take, and what the system does when retries run out.

---

## 🔁 Module 6 · Before / After

**Before:** after Module 5 the service stored its data well, but ran blind and brittle: no logs or metrics, settings in code, slow repeated website reads, timeouts treated as missing websites, and a restarted run duplicating its results.

*File: [`projects/company-enricher/stages/05-design-data/enricher/core/enrich.py`](../projects/company-enricher/stages/05-design-data/enricher/core/enrich.py)*

```python
try:
    page = self._websites.about_page(company.name)
except WebsiteUnavailable:
    result = EnrichmentResult(company, Outcome.NEEDS_REVIEW, ReviewReason.NO_WEBSITE, None, None, self._clock())
    self._store.save(result)
    return result
```

**After:** the service logs a structured event and updates metrics for every company, alerts on a high review rate, takes its settings and flags from the environment, runs every stage's tests on each push, caches pages within a run, retries temporary failures with backoff, degrades to review when a source is down, and records each result once even when a run is repeated.

*File: [`projects/company-enricher/stages/06-operate/enricher/app.py`](../projects/company-enricher/stages/06-operate/enricher/app.py)*

```python
def build_enricher(settings, about_urls=None):
    if settings.use_http_source:
        source = HttpWebsiteSource(about_urls or {})
    else:
        source = SampleWebsiteSource()
    source = CachingWebsiteSource(RetryingWebsiteSource(source, attempts=settings.retry_attempts))
    return Enricher(
        source,
        KeywordCategoryClassifier(),
        SqliteResultStore(settings.database_path),
        policy=SuggestionPolicy(settings.minimum_confidence),
        run_id=new_run_id(),
    )
```

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 10, "Define Errors Out Of Existence" (to verify against book).
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: masking and aggregating failures so callers see fewer of them.
2. **[RFC 9110, HTTP Semantics: idempotent methods](https://www.rfc-editor.org/rfc/rfc9110#name-idempotent-methods)**
   - Why: the standard definition of idempotency for web requests.
3. **[SQLite: UPSERT](https://www.sqlite.org/lang_upsert.html)**
   - Why: `ON CONFLICT ... DO NOTHING`, used for idempotent saves.
4. **[Python documentation: built-in exceptions, OSError and TimeoutError](https://docs.python.org/3/library/exceptions.html#os-exceptions)**
   - Why: which network errors are which.
5. **Book coverage for retries, timeouts, and idempotency:** none in the three books' freely available material; official documentation only.
   - Why: a book source should be chosen when the full books are available.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is the difference between a transient and a permanent failure, in this service?
2. **Application:** The website source starts answering every request with an error page instead of timing out. Which part of the design must change?
3. **Connection:** Look back at Day 3's inherited script. Which lessons does today's code rely on?
4. **Personal:** You started with an AI-written script you couldn't read. What would you now check first in the next one you inherit?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**You have finished the course.**
The Company Enricher started as a working script with names like `run`, `xs`, and `t`.
It is now a service you can read, change safely, explain in the business's language, store and evolve, watch, roll back, and trust when things fail.

**Where to go next:**

- Read the three main books in full, starting with *A Philosophy of Software Design*.
- Inherit a real script, at work or in an open-source project, and apply the Day 1-3 reading steps before changing anything.
- Revisit any day whose checklist you could not tick.

**Before you close the course, make sure you can:**

- [ ] Separate temporary from permanent failures and retry only the first.
- [ ] Explain how an idempotency key makes a repeated run safe.
- [ ] Describe the service's degraded mode and how a reviewer would recognise it.

[← Previous: Day 23 Measure before optimizing](./day-23-measure-before-optimizing.md) | [Course Home](../README.md)
