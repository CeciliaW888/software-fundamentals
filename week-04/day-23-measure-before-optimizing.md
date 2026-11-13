# Day 23: Measure before optimizing

[← Previous: Day 22 Deploy reversibly](./day-22-deploy-reversibly.md) | [Course Home](../README.md) | [Next: Day 24 Design for expected failure →](./day-24-design-for-failure.md)

> 📍 **Where we are in the story:** Week 4 · The service is almost ready for production. Now you run it, watch it, and recover when it fails.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Time each step of a batch to find where the time actually goes.
2. Use a profiler to confirm the critical path.
3. Choose the one change that attacks the slowest step.
4. Compare before and after with the same benchmark, and keep a test for the improvement.

**Plain idea:** guesses about speed are usually wrong, so measure first, change one thing, and measure again.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 6 · Operate what you build (lesson 0023)

---

## 📚 Core Concepts

### Observe: the batch is slow; what is slow?

Day 21's duration metrics show the nightly batch getting slower as more companies are added, and the same companies often appear several times in a batch.
Someone suggests rewriting the keyword classifier "because it loops over every word for every category".
It sounds plausible.
Before changing anything, measure.

The project has a benchmark: `python -m enricher.benchmark` in `stages/06-operate`.
It runs every sample company three times through a website source that waits 20 ms per page, standing in for a real network round trip, and times each step separately.
On one run of the benchmark on a laptop, the output was:

| Step | Time for 33 companies |
|---|---|
| read website | about 900 ms |
| classify | about 3 ms |

Your numbers will differ, but the shape will not: reading the website takes hundreds of times longer than classifying.
Rewriting the classifier could save at most a few milliseconds.

### Say it plainly: attack the biggest step, and only that

Once you know where the time goes, the options narrow.
The website step is slow because of waiting, not computing, and the same company's page is read three times per batch.
So the change is: remember each About page already read in this run.

`CachingWebsiteSource` wraps any website source and keeps successful pages in a dictionary for the life of the run.
It is another adapter behind Day 10's boundary, so nothing in the core changes.
On the same benchmark run, the batch went from about 920 ms without the cache to about 330 ms with it: each company's page is now fetched once instead of three times.

Two rules kept this honest:

- **Same benchmark before and after.** The comparison is only fair if nothing else changed.
- **A test for the improvement.** `test_cache_reads_each_website_once_per_run` checks the behaviour that makes it faster, so a later change cannot quietly undo it. The test counts calls rather than measuring milliseconds, because timing tests are flaky on shared machines.

For a fuller picture, `python -m enricher.benchmark --profile` runs the batch under Python's `cProfile`, which reports how much time is spent inside each function.

### Name it: critical path, profiling, caching

John Ousterhout's *A Philosophy of Software Design*, Chapter 20, "Designing for Performance" (to verify against book), advises measuring before modifying, because intuitions about performance are unreliable, and then focusing on the **critical path**, the small part of the code where most of the time is spent.
He also argues for designs that are naturally efficient without making them more complex; the cache is a small adapter, not a change to the core.

A **benchmark** is a repeatable measurement of performance.
A **profiler** measures how much time a program spends in each function.
A **cache** stores results so repeated requests can be answered without redoing the work.

*The Pragmatic Programmer*'s Topic 39, "Algorithm Speed" (to verify against book), makes the same demand; its Tip 64 (p. 208 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)) is "Test Your Estimates".
Ousterhout's free extract also notes, in Chapter 6, that removing special cases can make code faster as well as simpler, a theme he develops in Chapter 20 (to verify against book).

> **Key Insight:** The slow part is rarely the part that looks slow. Let a measurement choose what to optimise.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Critical path** | The small part of a program where most of its time is spent. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 20 (to verify against book) |
| **Benchmark** | A repeatable measurement of how fast something runs. | Standard software vocabulary; this plain definition is course-authored |
| **Profiler** | A tool that measures how much time a program spends in each function. | Official Python vocabulary ([The Python Profilers](https://docs.python.org/3/library/profile.html)) |
| **Cache** | A store of earlier results, used to answer repeated requests without redoing the work. | Standard software vocabulary; this plain definition is course-authored |
| **Latency** | The time between asking for something and getting it. | Standard software vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: Timing each step separately

*File: [`projects/company-enricher/stages/06-operate/enricher/benchmark.py`](../projects/company-enricher/stages/06-operate/enricher/benchmark.py)*

```python
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
```

**What's happening:** each step gets its own timer, so the result says where the time went, not just how much there was.

### Example 2: The one change the measurement chose

*File: [`projects/company-enricher/stages/06-operate/enricher/adapters/caching.py`](../projects/company-enricher/stages/06-operate/enricher/adapters/caching.py)*

```python
class CachingWebsiteSource:
    def __init__(self, inner):
        self._inner = inner
        self._pages = {}

    def about_page(self, company_name):
        if company_name not in self._pages:
            self._pages[company_name] = self._inner.about_page(company_name)
        return self._pages[company_name]
```

**What's happening:** if the inner source raises, nothing is stored, so failures are never cached.

### Example 3: A test for the improvement, not the stopwatch

*File: [`projects/company-enricher/stages/06-operate/tests/test_performance.py`](../projects/company-enricher/stages/06-operate/tests/test_performance.py)*

```python
def test_cache_reads_each_website_once_per_run():
    inner = CountingSource()
    cached = CachingWebsiteSource(inner)

    for _ in range(3):
        cached.about_page("Saltwater Kitchen")

    assert inner.calls == 1
```

> **💡 Try it:** in `stages/06-operate`, run `python -m enricher.benchmark`, then `python -m enricher.benchmark --profile`, and find `time.sleep` near the top of the profile.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. The benchmark shows website reads take about 900 ms and classification about 3 ms. What should you optimise?**

- A. Reading websites, the critical path
- B. The classifier, because its loops look slow
- C. Both equally
- D. Nothing; benchmarks are unreliable

<details>
<summary>Answer</summary>

**A.** Even a perfect classifier would save a few milliseconds. The measurement points at website reads.

</details>

**Q2. Why does the test count calls instead of asserting a time limit?**

- A. Counting is more accurate than timing.
- B. Timing tests are flaky on shared machines; the call count checks the cause of the speed-up reliably.
- C. Python cannot measure time in tests.
- D. To make the test faster.

<details>
<summary>Answer</summary>

**B.** The behaviour that makes it faster, one read per company, is deterministic; milliseconds are not.

</details>

**Q3. Why does the cache not store failed lookups?**

- A. Failures are too big to store.
- B. Dictionaries cannot hold exceptions.
- C. A temporary failure would otherwise be repeated for the rest of the run.
- D. It would be slower.

<details>
<summary>Answer</summary>

**C.** Caching a failure turns one bad moment into many. Only successful pages are remembered.

</details>

### Exercise 2 · Change: measure a second idea (⏱️ ~20 min)

**Goal:** Let numbers decide.

**Instructions:**
1. Hypothesis: "building the keyword sets on every call makes classification slow".
2. Write a micro-benchmark with `timeit` that calls `KeywordCategoryClassifier().suggest` on one About page 10,000 times.
3. Compare its total with the website step from `python -m enricher.benchmark`.
4. Write one sentence: is this worth optimising? Why or why not?

<details>
<summary>Hint</summary>

`timeit.timeit(lambda: classifier.suggest(text), number=10_000)` returns seconds for all 10,000 calls. Divide to compare per-company costs.

</details>

### Exercise 3 · Transfer: measure one slow thing (⏱️ ~10 min)

Pick something you believe is slow in a system you use.
Write how you would time each of its steps separately, and what result would prove your belief wrong.

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 20, "Designing for Performance" (to verify against book).
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: measure first, then find the critical path.
2. **[Python documentation: The Python Profilers](https://docs.python.org/3/library/profile.html)**
   - Why: how `cProfile` and `pstats` work.
3. **[Python documentation: timeit](https://docs.python.org/3/library/timeit.html)**
   - Why: timing small pieces of code reliably.
4. **[Python documentation: time.perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter)**
   - Why: the clock used by the benchmark.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is the critical path of the Company Enricher's batch?
2. **Application:** With real websites, the cache helps only within one run. What would a cache across runs need to handle?
3. **Connection:** How did Day 10's boundary make adding a cache a one-file change?
4. **Critical Thinking:** When could a cache make the service wrong rather than just faster?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 24: Design for expected failure](./day-24-design-for-failure.md). The last lesson: websites will fail; you decide in advance what the service does when they do.

**Before moving on, make sure you can:**

- [ ] Time each step of a process separately.
- [ ] Read a `cProfile` report's top lines.
- [ ] Justify one optimisation with a before-and-after measurement.

[← Previous: Day 22 Deploy reversibly](./day-22-deploy-reversibly.md) | [Course Home](../README.md) | [Next: Day 24 Design for expected failure →](./day-24-design-for-failure.md)
