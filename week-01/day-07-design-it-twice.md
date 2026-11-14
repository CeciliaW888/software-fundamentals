# Day 7: Design it twice

[← Previous: Day 6 Split by information, not length](./day-06-split-by-information.md) | [Course Home](../README.md) | [Next: Day 8 Decide what each failure means →](../week-02/day-08-what-each-failure-means.md)

> 📍 **Where we are in the story:** Week 1 · You can read the script now. Before it grows, you learn to tame its complexity.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Sketch two different interfaces for the same job before writing either.
2. Compare them with explicit criteria instead of taste.
3. Choose the Company Enricher's public operation and explain the choice.
4. Run the whole service end to end as a tracer bullet.

**Plain idea:** your first design is rarely your best; a second one gives you something to compare.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 2 · Control complexity (lesson 0007)

---

## 📚 Core Concepts

### Observe: two ways to ask for a category

The service needs one public operation that the rest of a system will call.
Here are two candidates, both able to use the deep modules from Days 5 and 6.

**Design A:** `enrich(company_name)` returns a `CategorySuggestion` when confident, `None` when not, and raises `WebsiteUnavailable` when there is no website.
This is the Module 1 shape.

**Design B:** `enrich(company_name)` always returns an `EnrichmentResult` with a status (`"accepted"` or `"needs_review"`), the suggestion, and the evidence: the URL and the sentence it came from.

Imagine the code that calls each design.
A reviewer screen needs to show weak cases with their evidence.
With Design A, `None` carries no evidence and no category, so the screen would have to call the website and classifier again.
With Design B, every result already has what the screen needs.

### Say it plainly: compare with criteria

Write the criteria down before you choose:

| Criterion | Design A: suggestion or `None` | Design B: always a result |
|---|---|---|
| What a caller must handle | three cases: value, `None`, exception | one type, with a status field |
| Evidence for reviewers | lost on `None` | always included |
| Room to grow | new outcomes need new return shapes | new statuses fit the same type |
| Cost to build | a little less code | one extra small class |

Design B wins on everything that callers feel, and loses only on a few lines of code.
That trade is almost always worth it, because a module is built once and used many times.

### Name it: design it twice, tracer bullets, prototypes

John Ousterhout's *A Philosophy of Software Design*, Chapter 11, "Design it Twice", recommends considering at least two radically different designs for each major decision, and comparing them on what matters most, such as the simplicity of the interface.
Even when the first idea wins, the comparison shows you why.

*The Pragmatic Programmer* offers two ways to test a design cheaply.
Topic 12, "Tracer Bullets" describes building a thin version that runs end to end through every part of the system, then filling it in.
Topic 13, "Prototypes and Post-it Notes" describes throwaway experiments that answer one question and are then discarded.

The Module 2 project has a tracer bullet: `python -m enricher` runs every sample company through the real website module, classifier, and store, and prints one line each.
It is small, but it is real code you keep and grow.

Three tips in the publisher's [official list of the book's tips](https://pragprog.com/tips/) sum up today's methods: Tip 20 (p. 51), "Use Tracer Bullets to Find the Target", Tip 21 (p. 57), "Prototype to Learn", and Tip 68 (p. 218), "Build End-To-End, Not Top-Down or Bottom Up".

> **Key Insight:** Write the caller's code for each design before choosing; the better interface is the one that makes calling code simpler.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Design it twice** | Considering two or more substantially different designs before choosing one. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 11 |
| **Tracer bullet** | A thin, working path through every layer of a system, kept and filled in over time. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 12, "Tracer Bullets" |
| **Prototype** | A throwaway experiment built to answer one specific question. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 13, "Prototypes and Post-it Notes" |
| **Result object** | A value that always comes back from an operation and describes what happened. | Course-authored plain definition |
| **Status** | A field on a result that says which outcome happened, such as accepted or needs review. | Course-authored plain definition |

---

## 💻 Code Examples

### Example 1: Design B, the chosen result type

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/enricher.py`](../projects/company-enricher/stages/02-control-complexity/enricher/enricher.py)*

```python
@dataclass(frozen=True)
class EnrichmentResult:
    company_name: str
    status: str
    suggestion: CategorySuggestion
    evidence_url: str
    evidence_text: str
```

**What's happening:** every call returns this, so a reviewer screen, a report, and a log line can all use the same fields.

### Example 2: The public operation

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/enricher.py`](../projects/company-enricher/stages/02-control-complexity/enricher/enricher.py)*

```python
def enrich(self, company_name):
    """Suggest a category for one company, with its evidence.

    Always returns an EnrichmentResult. Its status is "accepted" when
    confidence reaches the minimum, and the result is then saved;
    otherwise it is "needs_review" and nothing is saved.
    Raises WebsiteUnavailable when no About page can be read.
    """
    page = self._websites.about_page(company_name)
    suggestion = self._classifier.suggest(page.main_activity)
    accepted = suggestion.confidence >= self._minimum_confidence
    result = EnrichmentResult(
        company_name=company_name,
        status=ACCEPTED if accepted else NEEDS_REVIEW,
        suggestion=suggestion,
        evidence_url=page.url,
        evidence_text=page.main_activity,
    )
    if accepted:
        self._store.save(result)
    return result
```

**What's happening:** one missing website still raises an exception here.
That is a deliberate loose end: Day 8 decides what that failure should mean.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why does a reviewer screen favour Design B?**

- A. Weak results still carry the suggestion and its evidence.
- B. It runs faster.
- C. It never needs a website.
- D. It has fewer classes.

<details>
<summary>Answer</summary>

**A.** With Design A a weak case returns None and the evidence is lost. Design B keeps it on every result.

</details>

**Q2. What is the main difference between a tracer bullet and a prototype?**

- A. A prototype runs end to end; a tracer bullet does not.
- B. A tracer bullet is kept and grown; a prototype is thrown away.
- C. Only prototypes have tests.
- D. There is no difference.

<details>
<summary>Answer</summary>

**B.** Tracer-bullet code is the real skeleton of the system. A prototype answers one question and is discarded.

</details>

**Q3. What should you write first when comparing two interfaces?**

- A. The full implementation of both
- B. A performance benchmark
- C. The calling code each design would need
- D. The database schema

<details>
<summary>Answer</summary>

**C.** The caller's code shows the cost of an interface directly. Implementations can wait until you have chosen.

</details>

### Exercise 2 · Change: write the calling code twice (⏱️ ~15 min)

**Goal:** Let the caller decide.

**Instructions:**
1. Write a function `print_review_list(company_names)` that prints every company needing review with the sentence that was used as evidence.
2. Write it once against Design A (use `suggest_company_category` from `stages/01-read-code`) and once against Design B (`Enricher.enrich` from `stages/02-control-complexity`).
3. Compare the two functions line by line.
4. Run the tracer bullet: `cd stages/02-control-complexity && python -m enricher`.

<details>
<summary>Hint</summary>

With Design A you will find you need to call `read_about_page` again for every `None`, because the evidence was thrown away.

</details>

### Exercise 3 · Transfer: two designs for one decision (⏱️ ~10 min)

Pick a function you are about to write.
Sketch two signatures that differ in what they return, not just in names.
Write the three-line caller for each and pick one.

---

## 🔁 Module 2 · Before / After

**Before:** after Module 1 the code was readable but tangled: category knowledge in several places, a three-step website chain that every caller had to follow, and a main function whose `None` threw away the evidence.

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
website = find_official_website(
    company_name
)
about_text = read_about_page(website)
activity_summary = (
    summarise_business_activity(
        about_text
    )
)
suggestion = classifier.suggest(
    activity_summary
)
```

**After:** category knowledge lives in `categories.py`, websites sit behind one deep module, the classifier is one readable function, and the public operation always returns a result with evidence.
The decisions for every sample company are unchanged, and a tracer bullet runs the whole service.

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/__main__.py`](../projects/company-enricher/stages/02-control-complexity/enricher/__main__.py)*

```python
enricher = Enricher(CompanyWebsites(), KeywordCategoryClassifier(), InMemoryResultStore())
for company_name in SAMPLE_WEB:
    result = enricher.enrich(company_name)
    print(f"{company_name:22} {result.status:13} {result.suggestion.category} ({result.suggestion.confidence:.2f})")
```

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 11, "Design it Twice".
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: how and why to compare alternatives.
2. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topics 12, "Tracer Bullets" and 13, "Prototypes and Post-it Notes".
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: two cheap ways to test a design.
3. **[Python documentation: `__main__`](https://docs.python.org/3/library/__main__.html)**
   - Why: how `python -m enricher` finds and runs the tracer bullet.

---

## 🤔 Reflection Questions

1. **Comprehension:** Which criterion in the comparison table mattered most to you, and why?
2. **Application:** Design C returns a list of results for a list of names. When would that beat Design B?
3. **Connection:** How did Days 5 and 6 make Design B cheap to build?
4. **Personal:** Think of an interface you use that you wish had been designed twice. What would the second design have been?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 8: Decide what each failure means](../week-02/day-08-what-each-failure-means.md). Module 3 begins: you learn to change the service without breaking what works.

**Before moving on, make sure you can:**

- [ ] Compare two interfaces with written criteria.
- [ ] Explain why Design B returns a result even when confidence is low.
- [ ] Run the tracer bullet and read its output.

[← Previous: Day 6 Split by information, not length](./day-06-split-by-information.md) | [Course Home](../README.md) | [Next: Day 8 Decide what each failure means →](../week-02/day-08-what-each-failure-means.md)
