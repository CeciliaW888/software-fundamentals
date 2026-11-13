# Day 8: Decide what each failure means

[← Previous: Day 7 Design it twice](../week-01/day-07-design-it-twice.md) | [Course Home](../README.md) | [Next: Day 9 Tests are executable evidence →](./day-09-tests-are-evidence.md)

> 📍 **Where we are in the story:** Week 2 · The structure is clearer. Now you learn to change it without breaking what already works.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Sort the Company Enricher's failures into expected business cases and programming errors.
2. Choose one of four responses for each: prevent, hide, combine, or report.
3. Turn "no website" into a result that sends the company to review instead of crashing.
4. Make an impossible value stop the program at once.

**Plain idea:** every failure needs a decision about what it means, made on purpose and written down.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 3 · Change safely (lesson 0008)

---

## 📚 Core Concepts

### Observe: what can go wrong today

Run the Module 2 tracer bullet with one extra company, Ghost Gum Traders, which has no website.
The whole batch stops with a `WebsiteUnavailable` traceback.
Ten good results are lost because of one missing website.

List every way the service can go wrong:

1. A company has no website, or the page cannot be read.
2. The About page has no category keywords.
3. A classifier returns a confidence of 1.7, which is impossible.
4. Saving a result fails.

These are not the same kind of problem.
The first two happen every day with real companies.
The third means the code is wrong.
The fourth means something outside the service is broken.

### Say it plainly: four things you can do with a failure

For each failure you have four choices.

- **Prevent it.** Change the rules so the situation is not an error. No keywords is not an error; it just means the category is Other with confidence 0.0, which already goes to review.
- **Hide it.** Handle it inside the module so callers never see it. "No website" becomes a result with status `needs_review` and reason `no_website`.
- **Combine it.** Handle many similar failures in one place. Every review reason flows through the same result type, so a reviewer screen handles them all the same way.
- **Report it.** Stop and tell someone. An impossible confidence means a bug, so the service raises `ValueError` immediately rather than saving nonsense.

Store failures are left to report themselves: hiding a failed save would lose data silently.

### Name it: define errors out of existence, crash early

John Ousterhout's *A Philosophy of Software Design*, Chapter 10, "Define Errors Out Of Existence" (to verify against book), argues that exceptions add complexity to every caller, and that the best way to reduce it is to design so that fewer exceptions are needed.
He describes defining errors out of existence, **exception masking** (handling a condition at a low level so higher levels never see it), and **exception aggregation** (handling many exceptions in one place).
He also notes that some errors are best handled by simply crashing, when recovery is not worth the complexity.

*The Pragmatic Programmer* makes the crash case in Topic 24, "Dead Programs Tell No Lies" (to verify against book): when code finds something that should be impossible, stopping usually does less harm than carrying on with bad data.
Topic 25, "Assertive Programming" (to verify against book) recommends checking for the impossible in code, so the check fails loudly if it ever happens.
In this service, `check_confidence` plays that role with an explicit `ValueError`, which unlike `assert` cannot be switched off.

Two tips in the publisher's [official list of the book's tips](https://pragprog.com/tips/) name the rule directly: Tip 38 (p. 113), "Crash Early", and Tip 39 (p. 115), "Use Assertions to Prevent the Impossible".

> **Key Insight:** Expected situations become normal results; impossible situations stop the program. Do not mix the two.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Exception** | A Python object that signals an error and interrupts normal flow until something handles it. | Official Python vocabulary ([tutorial: errors and exceptions](https://docs.python.org/3/tutorial/errors.html)) |
| **Exception masking** | Handling an exceptional condition at a low level so higher levels never see it. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 10 (to verify against book) |
| **Exception aggregation** | Handling many exceptions with one piece of code instead of many. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 10 (to verify against book) |
| **Crash early** | Stopping as soon as the code finds an impossible state, instead of continuing with bad data. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 24, "Dead Programs Tell No Lies" (to verify against book) |
| **Review reason** | Why a result needs a person: weak evidence or no website. | Course domain term |

---

## 💻 Code Examples

### Example 1: "No website" becomes a result

*File: [`projects/company-enricher/stages/03-change-safely/enricher/enricher.py`](../projects/company-enricher/stages/03-change-safely/enricher/enricher.py)*

```python
try:
    page = self._websites.about_page(company_name)
except WebsiteUnavailable:
    return self._needs_review(company_name, NO_WEBSITE)
```

**What's happening:** the exception is masked inside `enrich`.
Callers get a normal `EnrichmentResult` with status `needs_review` and reason `no_website`, and the batch carries on.

### Example 2: An impossible value stops the program

*File: [`projects/company-enricher/stages/03-change-safely/enricher/enricher.py`](../projects/company-enricher/stages/03-change-safely/enricher/enricher.py)*

```python
def check_confidence(confidence):
    """A confidence outside 0..1 is a bug in a classifier: stop at once."""
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"confidence must be between 0 and 1, got {confidence!r}")
```

**What's happening:** `enrich` calls this on every suggestion before using it.
A broken classifier is reported loudly instead of producing confident nonsense.

### Example 3: An error defined out of existence

*File: [`projects/company-enricher/stages/03-change-safely/enricher/classifier.py`](../projects/company-enricher/stages/03-change-safely/enricher/classifier.py)*

```python
if total_hits == 0:
    return CategorySuggestion(OTHER, 0.0)
```

**What's happening:** text without keywords is a normal answer, Other with zero confidence, and the review rule handles it like any other weak suggestion.

> **💡 Try it:** run `python -m enricher` in `stages/03-change-safely`. Ghost Gum Traders now prints `needs_review  no_website` instead of stopping the run.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. A company's About page has no category keywords. What does the service do?**

- A. Raise an exception
- B. Retry the website
- C. Skip the company silently
- D. Return Other with confidence 0.0, which goes to review

<details>
<summary>Answer</summary>

**D.** The situation is defined out of existence: it is a normal, weak suggestion, not an error.

</details>

**Q2. Why does an impossible confidence raise instead of being sent to review?**

- A. It can only come from a bug, and continuing would spread bad data.
- B. Reviewers are too busy.
- C. Python cannot store numbers above 1.
- D. Exceptions are faster than results.

<details>
<summary>Answer</summary>

**A.** Impossible states mean the program is wrong. Crashing early stops the damage and points straight at the cause.

</details>

**Q3. Which failure does the service deliberately leave unhandled?**

- A. No website
- B. A failed save to the store
- C. No keywords
- D. Weak evidence

<details>
<summary>Answer</summary>

**B.** Hiding a failed save would silently lose a result, so it is left to report itself to the caller.

</details>

### Exercise 2 · Change: design a new failure (⏱️ ~15 min)

**Goal:** Decide what "the About page is empty" means.

**Instructions:**
1. Look at `HttpWebsiteSource.about_page` in `stages/03-change-safely/enricher/website.py`. What does it do when the page has no text?
2. Decide which of the four responses fits, and write one sentence explaining why.
3. Write a test in `tests/test_http_source.py` that pins your decision, using a fake `fetch` that returns `"<html></html>"`.
4. Run `python -m pytest -q`.

<details>
<summary>Hint</summary>

The adapter raises `WebsiteUnavailable`, which `enrich` already masks as `no_website`. Your test only needs to check that the adapter raises.

</details>

### Exercise 3 · Transfer: label your failures (⏱️ ~10 min)

Pick a function you know that raises or catches exceptions.
For each one, write "expected" or "impossible", then prevent, hide, combine, or report.
Find one that is in the wrong group.

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 10, "Define Errors Out Of Existence" (to verify against book).
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: masking, aggregation, and when to crash.
2. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topics 24, "Dead Programs Tell No Lies" and 25, "Assertive Programming" (to verify against book).
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: stopping on the impossible.
3. **[Python tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)**
   - Why: how `try`, `except`, and `raise` work.
4. **[Python reference: the assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)**
   - Why: explains why assertions disappear when Python runs with optimisation, which is why this service raises `ValueError` instead.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is the difference between hiding a failure and ignoring it?
2. **Application:** A website returns a page in a language the keywords do not cover. Which response fits?
3. **Connection:** How did Day 7's result type make masking "no website" easy?
4. **Critical Thinking:** Could masking too many failures make a service look healthy when it is not? How would you notice?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 9: Tests are executable evidence](./day-09-tests-are-evidence.md). You will turn each promise and failure decision into a test.

**Before moving on, make sure you can:**

- [ ] Sort failures into expected and impossible.
- [ ] Choose prevent, hide, combine, or report for each.
- [ ] Explain why the service raises `ValueError` rather than using `assert`.

[← Previous: Day 7 Design it twice](../week-01/day-07-design-it-twice.md) | [Course Home](../README.md) | [Next: Day 9 Tests are executable evidence →](./day-09-tests-are-evidence.md)
