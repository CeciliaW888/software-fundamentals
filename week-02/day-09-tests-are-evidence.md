# Day 9: Tests are executable evidence

[← Previous: Day 8 Decide what each failure means](./day-08-what-each-failure-means.md) | [Course Home](../README.md) | [Next: Day 10 Put volatile dependencies at boundaries →](./day-10-volatile-dependencies.md)

> 📍 **Where we are in the story:** Week 2 · The structure is clearer. Now you learn to change it without breaking what already works.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Turn each promise in a docstring into one focused test.
2. Use pytest fixtures to build the service once for many tests.
3. Pin current behaviour with a parametrized characterization test.
4. Write a property-style test that checks a rule for many generated inputs.

**Plain idea:** a test is a promise you can run; if it passes, you have evidence, not just hope.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 3 · Change safely (lesson 0009)

---

## 📚 Core Concepts

### Observe: one docstring, four tests

The docstring of `Enricher.enrich` in stage 03 makes four promises:

1. A confident suggestion is accepted and saved.
2. Weak evidence needs review and is not saved.
3. A missing website needs review instead of crashing.
4. Every result records when it was checked.

Open `tests/test_promises.py`.
It has exactly four tests, one per promise, and each test's name reads like the promise.
None of them checks which helper was called, how keywords are counted, or what the page URL looks like.
They check what a caller can observe: the status, the reason, and what the store contains.

### Say it plainly: three kinds of evidence

The stage 03 tests come in three kinds, and each answers a different question.

- **Promise tests** answer "does it do what the docstring says?". One test per promise.
- **Characterization tests** answer "did my change alter any decision?". `test_same_decisions.py` lists every sample company with the category it should get, and runs one test per company.
- **Property tests** answer "does a rule hold for inputs nobody thought of?". `test_properties.py` builds 200 random texts from category keywords and checks that every suggestion has a known category and a confidence between 0 and 1.

A good suite needs all three.
Promise tests explain the design, characterization tests guard refactoring, and property tests find the cases your examples missed.

Tests are only evidence if they cannot be fooled by the outside world.
That is why the tests use a fixed clock time and the sample website source: they give the same answer on every machine, every day.

### Name it: fixtures, parametrize, properties

pytest calls the shared setup a **fixture**: a function marked with `@pytest.fixture` whose return value is passed to any test that names it as a parameter.
`@pytest.mark.parametrize` runs one test function once for each set of arguments.

*The Pragmatic Programmer*'s Topic 41, "Test to Code" argues that thinking about how to test a piece of code improves its design, because testable code tends to be decoupled code.
You saw that happen: the injectable clock exists because a test needed a fixed time.
Topic 42, "Property-Based Testing" describes checking invariants with generated inputs rather than hand-picked examples.
The book's examples use a dedicated library; this project uses Python's `random` module with fixed seeds so it needs nothing beyond pytest, and the Hypothesis library is a good next step.

The book's testing tips in the publisher's [official list of the book's tips](https://pragprog.com/tips/) add two angles worth remembering.
Tip 67 (p. 216), "A Test Is the First User of Your Code": a test is the first caller to feel how easy or awkward an interface is.
Tip 69 (p. 221), "Design to Test": code that is hard to test is usually telling you something about its design.

> **Key Insight:** Test what callers can observe. Tests of internal steps break when you improve the code; tests of promises protect you while you do.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Test** | Code that runs other code and checks one expected behaviour. | Course-authored plain definition |
| **Fixture** | A pytest function that prepares something tests need and passes it to them by name. | Official pytest vocabulary ([fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)) |
| **Parametrized test** | One test function run once for each set of arguments. | Official pytest vocabulary ([parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)) |
| **Characterization test** | A test that pins what the code does today, so a change that alters it fails. | Standard software vocabulary; this plain definition is course-authored |
| **Property-based test** | A test that checks a rule holds for many generated inputs. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 42, "Property-Based Testing" |
| **Deterministic** | Giving the same result every time it runs with the same inputs. | Course-authored plain definition |

---

## 💻 Code Examples

### Example 1: A fixture that builds the service

*File: [`projects/company-enricher/stages/03-change-safely/tests/conftest.py`](../projects/company-enricher/stages/03-change-safely/tests/conftest.py)*

```python
FIXED_TIME = datetime(2026, 1, 5, 9, 30, tzinfo=timezone.utc)


@pytest.fixture
def store():
    return InMemoryResultStore()


@pytest.fixture
def enricher(store):
    return Enricher(SampleWebsiteSource(), KeywordCategoryClassifier(), store, clock=lambda: FIXED_TIME)
```

**What's happening:** every test that asks for `enricher` gets a fresh service with a fixed clock, and can also ask for the same `store` to inspect what was saved.

### Example 2: One promise, one test

*File: [`projects/company-enricher/stages/03-change-safely/tests/test_promises.py`](../projects/company-enricher/stages/03-change-safely/tests/test_promises.py)*

```python
def test_missing_website_needs_review_instead_of_crashing(enricher, store):
    result = enricher.enrich("Ghost Gum Traders")

    assert result.status == NEEDS_REVIEW
    assert result.reason == NO_WEBSITE
    assert store.saved_results == []
```

**What's happening:** the test reads like Day 8's decision.
If someone removes the `try`/`except`, this test fails with a clear name.

### Example 3: A property that must always hold

*File: [`projects/company-enricher/stages/03-change-safely/tests/test_properties.py`](../projects/company-enricher/stages/03-change-safely/tests/test_properties.py)*

```python
@pytest.mark.parametrize("seed", range(200))
def test_any_text_gets_a_known_category_and_a_confidence_between_0_and_1(seed):
    rng = random.Random(seed)
    text = " ".join(rng.choice(VOCABULARY) for _ in range(rng.randint(0, 12)))

    suggestion = KeywordCategoryClassifier().suggest(text)

    assert suggestion.category in CATEGORIES
    assert 0.0 <= suggestion.confidence <= 1.0
```

**What's happening:** 200 different texts, including empty ones, each checked against the same rule.
Each seed always produces the same text, so a failure can be reproduced exactly.

> **💡 Try it:** in `stages/03-change-safely`, run `python -m pytest -q`. You should see 220 tests pass in well under a second.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which test is most likely to break when you improve the code without changing behaviour?**

- A. A test that the result's status is `needs_review`
- B. A test that the store is empty after weak evidence
- C. A test that `about_page` was called before `suggest`
- D. A test that confidence is between 0 and 1

<details>
<summary>Answer</summary>

**C.** Call order is an internal step. The other three check what callers can observe, which a refactoring keeps the same.

</details>

**Q2. Why does the fixture use a fixed clock?**

- A. To make tests run faster
- B. Because Python has no clock
- C. To test time zones
- D. So `checked_at` is the same on every run and can be asserted

<details>
<summary>Answer</summary>

**D.** A real clock gives a different time on every run. Injecting a fixed time makes the test deterministic.

</details>

**Q3. What does the property test find that example tests usually miss?**

- A. Inputs nobody thought to write down, such as empty text
- B. Slow code
- C. Spelling mistakes in names
- D. Missing documentation

<details>
<summary>Answer</summary>

**A.** Generated inputs explore cases beyond the hand-picked examples, such as text with no words at all.

</details>

### Exercise 2 · Change: test a new promise (⏱️ ~20 min)

**Goal:** Add a promise and prove it.

**Instructions:**
1. New promise: "the evidence text of every result that has a suggestion is the first sentence of the About page".
2. Add one line to the docstring of `Enricher.enrich` stating it.
3. Write one test for it in `tests/test_promises.py`, using the `enricher` fixture and a company of your choice.
4. Write a property-style test that checks the promise for every company in `SAMPLE_WEB`.
5. Run `python -m pytest -q` and make sure both pass.

<details>
<summary>Hint</summary>

`SAMPLE_WEB[name]["about"].split(".")[0]` is the expected evidence. Parametrize over `SAMPLE_WEB.keys()`.

</details>

### Exercise 3 · Transfer: map promises to tests (⏱️ ~10 min)

Pick a function with a docstring in a project you know.
List its promises, then list its tests.
Mark each promise that has no test, and each test that checks an internal step instead of a promise.

---

## 📖 Curated Resources

1. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topics 41, "Test to Code" and 42, "Property-Based Testing".
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: why testing shapes design, and testing with generated inputs.
2. **[pytest: how to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)**
   - Why: everything behind `conftest.py`.
3. **[pytest: how to parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)**
   - Why: one test function, many cases.
4. **[Hypothesis documentation](https://hypothesis.readthedocs.io/en/latest/)**
   - Why: a library for property-based testing in Python, for when the hand-rolled version runs out.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is the difference between a promise test and a characterization test?
2. **Application:** Which test would fail first if someone changed the threshold from 0.82 to 0.6?
3. **Connection:** How does Day 2's advice to test what callers can observe show up in `test_promises.py`?
4. **Critical Thinking:** Can a suite of passing tests still miss a real bug? Give one example for this service.

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 10: Put volatile dependencies at boundaries](./day-10-volatile-dependencies.md). You will put the website and the clock behind narrow adapters.

**Before moving on, make sure you can:**

- [ ] Write one test per docstring promise.
- [ ] Use a fixture and a parametrized test.
- [ ] Explain why tests must be deterministic.

[← Previous: Day 8 Decide what each failure means](./day-08-what-each-failure-means.md) | [Course Home](../README.md) | [Next: Day 10 Put volatile dependencies at boundaries →](./day-10-volatile-dependencies.md)
