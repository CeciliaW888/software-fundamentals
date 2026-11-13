# Day 16: Turn qualities into measurable requirements

[← Previous: Day 15 Distil the core](../week-02/day-15-distil-the-core.md) | [Course Home](../README.md) | [Next: Day 17 Choose a data model from access patterns →](./day-17-data-model-from-access.md)

> 📍 **Where we are in the story:** Week 3 · The model fits the business. Now the data it keeps has to evolve without breaking.

---

> **Book coverage:** *The Pragmatic Programmer* supports making quality an explicit requirement agreed with users (Tip 8 in the official tip list).
> How to measure quality, with indicators, targets, and percentiles, is not in the books' freely available material, so that part relies on Python's documentation and course-authored definitions.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Rewrite a vague quality ("fast", "accurate") as a measurable target.
2. Choose an indicator, a target, and a measurement method for each quality.
3. Explain why a percentile describes latency better than an average.
4. Turn quality targets into a test that fails when the service gets worse.

**Plain idea:** "good enough" means nothing until you say what you will measure, how, and what number counts as good.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 5 · Design data that can evolve (lesson 0016)

---

## 📚 Core Concepts

### Observe: three wishes nobody can check

Before the service gets a database, the team writes down what "working well" means.
The first draft says:

1. The service should be accurate.
2. It shouldn't send too much to review.
3. It should be fast.

Each line is true and useless.
Accurate compared with what?
How much review is too much?
Fast for whom, measured where?
Two people can read the same line and disagree about whether the service passes, which means it cannot guide any decision, including the data design in the next four days.

### Say it plainly: indicator, target, method

Each quality becomes three parts: what you measure, the number that counts as good, and how you measure it.

| Quality | Indicator | Target | How it is measured |
|---|---|---|---|
| Accurate | Of the results the service **suggests**, the share a person agrees with | at least 95% | run the labelled sample: 12 companies with a reviewer's decision |
| Not too much review | Share of companies that **need review** | at most 30% | the same run |
| Fast | Time to enrich one company, 95th percentile | at most 50 ms with the sample website source | `time.perf_counter()` around each call |

Notice the choices.
Accuracy only counts suggested results, because sending a hard case to review is the service working correctly, not a mistake.
Latency uses the 95th percentile: the time that 95% of calls beat.
An average hides the slow calls that people actually notice, and one very slow call can hide behind many fast ones.

Today the labelled sample says the service suggests 9 companies, all correctly, and sends 3 to review: precision 100%, review rate 25%.
Both meet their targets, with headroom.

The targets go into code, in `enricher/quality.py`, and a test, `test_quality.py`, checks them on every run.
If a change to the keywords drops precision, the build fails with a number, not an opinion.

### Name it: quality attributes, indicators, objectives

Requirements about how well a system works, rather than what it does, are often called **quality attributes** or **non-functional requirements**.
An **indicator** is a measured value, such as precision or 95th-percentile latency.
A **target** (in operations work often called an objective) is the value the indicator must meet.
A **percentile** is the value below which a given share of measurements fall.

These terms are standard across the industry; the definitions here are course-authored.
For timing, Python's `time.perf_counter()` gives a clock with the highest available resolution for measuring short durations.

*The Pragmatic Programmer*'s Topic 5, "Good-Enough Software" (to verify against book), treats quality as something the people who use the software should help decide, not something developers pick alone.
Its Tip 8 (p. 12 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)) is "Make Quality a Requirements Issue": the targets above are that tip written down as numbers.

> **Key Insight:** A quality you cannot measure cannot guide a design decision. Write the indicator, the target, and the method, then test them.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Quality attribute** | A requirement about how well a system works, such as speed or accuracy, rather than what it does. | Standard software vocabulary; this plain definition is course-authored |
| **Indicator** | A measured value that shows how well a quality is met. | Course-authored plain definition |
| **Target** | The value an indicator must meet for the quality to count as good. | Course-authored plain definition |
| **Precision** | Of the items the service labelled, the share it labelled correctly. | Standard data and machine-learning vocabulary; this plain definition is course-authored |
| **Percentile** | The value below which a given share of measurements fall; the 95th percentile is beaten by 95% of them. | Standard statistics vocabulary; this plain definition is course-authored |
| **Labelled sample** | Example inputs with the correct answer decided by a person, used to measure a system. | Course-authored plain definition |

---

## 💻 Code Examples

### Example 1: The targets, in code

*File: [`projects/company-enricher/stages/05-design-data/enricher/quality.py`](../projects/company-enricher/stages/05-design-data/enricher/quality.py)*

```python
QUALITY_TARGETS = {
    "minimum_precision": 0.95,  # of SUGGESTED results, the share that are right
    "maximum_review_rate": 0.30,  # share of companies sent to a person
    "maximum_p95_latency_ms": 50.0,  # per company, with the sample website source
}
```

**What's happening:** the three targets are data, in one place, with a comment saying exactly what each measures.

### Example 2: Measuring latency per call

*File: [`projects/company-enricher/stages/05-design-data/enricher/quality.py`](../projects/company-enricher/stages/05-design-data/enricher/quality.py)*

```python
started = time.perf_counter()
result = enricher.enrich(Company(company_id=f"sample:{number}", name=name))
latencies_ms.append((time.perf_counter() - started) * 1000)
```

**What's happening:** the timer wraps exactly one enrich call, so the measurement matches the indicator's definition.

### Example 3: The targets as a test

*File: [`projects/company-enricher/stages/05-design-data/tests/test_quality.py`](../projects/company-enricher/stages/05-design-data/tests/test_quality.py)*

```python
def test_the_service_meets_its_quality_targets():
    report = measure(Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), InMemoryResultStore()))

    assert report.precision >= QUALITY_TARGETS["minimum_precision"]
    assert report.review_rate <= QUALITY_TARGETS["maximum_review_rate"]
    assert report.p95_latency_ms <= QUALITY_TARGETS["maximum_p95_latency_ms"]
```

**What's happening:** a regression in any quality now fails the build with the measured number in the error.

> **💡 Try it:** in `stages/05-design-data`, run `python -c "from enricher.quality import measure; from enricher.core.enrich import Enricher; from enricher.adapters.website import SampleWebsiteSource; from enricher.core.classifier import KeywordCategoryClassifier; from enricher.adapters.store import InMemoryResultStore; print(measure(Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), InMemoryResultStore())))"`.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why does precision count only suggested results?**

- A. Review results are too slow to count.
- B. Python cannot count review results.
- C. To make the number look better.
- D. Sending a hard case to review is correct behaviour, not a wrong answer.

<details>
<summary>Answer</summary>

**D.** Precision asks "when the service commits to an answer, is it right?". Review cases are measured separately by the review rate.

</details>

**Q2. Why use the 95th percentile instead of the average for latency?**

- A. Averages hide the slow calls that people notice.
- B. It is easier to compute.
- C. Percentiles are always smaller.
- D. Python has no average function.

<details>
<summary>Answer</summary>

**A.** One very slow call can hide behind many fast ones in an average. The 95th percentile shows what nearly every caller experiences.

</details>

**Q3. Which statement is a measurable requirement?**

- A. The service should be fast.
- B. At most 30% of companies in the labelled sample need review.
- C. Reviewers should be happy.
- D. The service should rarely be wrong.

<details>
<summary>Answer</summary>

**B.** It names the indicator, the target, and where it is measured. The others cannot be checked.

</details>

### Exercise 2 · Change: break a target on purpose (⏱️ ~15 min)

**Goal:** See the quality test catch a regression.

**Instructions:**
1. In `stages/05-design-data/enricher/core/categories.py`, add `"paint"` to the Construction keywords (painters are a trade, after all).
2. Run `python -m pytest -q tests/test_quality.py`.
3. Read which target failed and by how much, then explain why from the sample data.
4. Undo the change.

<details>
<summary>Hint</summary>

Bluegum Hardware's first sentence says its store sells paint. Its confidence drops from 1.0 to about 0.67, it moves to review, and the review rate rises from 25% to 33%.

</details>

### Exercise 3 · Transfer: make one wish measurable (⏱️ ~10 min)

Pick one vague quality from a project you know ("reliable", "easy to use", "scalable").
Write an indicator, a target, and a way to measure it.
Then write down what decision the target would change.

---

## 📖 Curated Resources

1. **[Python documentation: time.perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter)**
   - Why: the right clock for timing short operations.
2. **[Python documentation: statistics](https://docs.python.org/3/library/statistics.html)**
   - Why: `statistics.quantiles` computes percentiles if you want more than the simple version in `quality.py`.
3. **Book coverage for measurement:** none in the three books' freely available material; official documentation only.
   - Why: a book source should be chosen when the full books are available.
4. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 5, "Good-Enough Software" (to verify against book).
   - 🔗 [Official tip list](https://pragprog.com/tips/)
   - Why: Tip 8, on making quality a requirement agreed with users.

---

## 🤔 Reflection Questions

1. **Comprehension:** What are the three parts of a measurable requirement?
2. **Application:** The business wants "reviewers spend less time per company". Write an indicator for it.
3. **Connection:** How do Day 9's tests and today's quality test differ in what they protect?
4. **Critical Thinking:** The labelled sample has 12 companies. What can and can't a sample that small tell you?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 17: Choose a data model from access patterns](./day-17-data-model-from-access.md). The review rate target needs a review queue; the queue needs a data model.

**Before moving on, make sure you can:**

- [ ] Rewrite a vague quality as indicator, target, and method.
- [ ] Explain precision and the 95th percentile in plain words.
- [ ] Turn a target into a test.

[← Previous: Day 15 Distil the core](../week-02/day-15-distil-the-core.md) | [Course Home](../README.md) | [Next: Day 17 Choose a data model from access patterns →](./day-17-data-model-from-access.md)
