# Day 11: Refactor under evidence

[← Previous: Day 10 Put volatile dependencies at boundaries](./day-10-volatile-dependencies.md) | [Course Home](../README.md) | [Next: Day 12 Build language from examples →](./day-12-language-from-examples.md)

> 📍 **Where we are in the story:** Week 2 · The structure is clearer. Now you learn to change it without breaking what already works.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Explain what makes a change a refactoring.
2. Put a characterization test in place before changing structure.
3. Refactor in small steps, running the tests and committing after each one.
4. Undo a bad step with version control instead of by hand.

**Plain idea:** change the shape of the code in small steps, with tests proving after each step that nothing else changed.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 3 · Change safely (lesson 0011)

---

## 📚 Core Concepts

### Observe: working code that could be clearer

Open `exercises/day11_before_refactor.py` in stage 03.
It holds the version of `enrich` that existed before today's lesson.
All 220 tests pass with it.
But look at how it builds the result: it calls `self._decide(suggestion)` twice, once for the status and once inside the expression for the reason.

Nothing is broken.
Yet a reader has to check that both calls give the same answer, and a future change to `_decide` (say, logging each decision) would now run twice.
This is the kind of small, real untidiness that refactoring is for.

### Say it plainly: the safe way to reshape code

A refactoring changes how the code is built without changing what it does.
The only way to know "what it does" stayed the same is evidence, and the cheapest evidence is a test suite you trust.

The safe loop is:

1. **Pin the behaviour.** Make sure tests cover what you might break. Stage 03 has `test_same_decisions.py`, which pins every sample company's decision, plus the promise tests from Day 9.
2. **Make one small change.** Here: compute the status once, store it in a variable, and use it twice.
3. **Run the tests.** All green means the step kept behaviour.
4. **Commit.** A commit per step gives you a known-good point to return to.
5. **Repeat or undo.** If a step turns the tests red and the fix is not obvious, do not debug forward; revert to the last commit and take a smaller step.

Mixing a refactoring with a behaviour change in the same step breaks the loop.
If the tests fail, you cannot tell which change caused it.

### Name it: refactoring, characterization tests, version control

*The Pragmatic Programmer*, Topic 40, "Refactoring" (to verify against book), describes refactoring as a disciplined restructuring of existing code that does not change its external behaviour, done in small steps with good tests.
The book's Topic 19, "Version Control" (to verify against book) argues for keeping everything in version control, so any step can be undone.

John Ousterhout's *A Philosophy of Software Design*, Chapter 16, "Modifying Existing Code" (to verify against book), adds the design view: when you change code, aim to leave the design better than you found it, as if it had been written that way from the start, rather than making the smallest possible patch.

Git provides the tools: `git commit` records a step; `git revert` creates a new commit that undoes an earlier one; `git restore` throws away uncommitted edits.

*The Pragmatic Programmer*'s Topic 27, "Don't Outrun Your Headlights", available as the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), explains why the steps stay small: take a step, get feedback, then decide the next one, instead of committing to a long plan you cannot see the end of.
Its tips in the publisher's [official list of the book's tips](https://pragprog.com/tips/) include Tip 42 (p. 126), "Take Small Steps - Always", Tip 65 (p. 212), "Refactor Early, Refactor Often", and Tip 28 (p. 85), "Always Use Version Control".

> **Key Insight:** Tests make refactoring safe, small steps make failures easy to locate, and commits make every step reversible.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Refactoring** | Restructuring existing code without changing its external behaviour. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 40, "Refactoring" (to verify against book) |
| **Characterization test** | A test that pins what the code does today, so a change that alters it fails. | Standard software vocabulary; this plain definition is course-authored |
| **Commit** | A saved snapshot of changes in Git, with a message explaining them. | Official Git vocabulary ([git-commit](https://git-scm.com/docs/git-commit)) |
| **Revert** | A new commit that undoes the changes of an earlier commit. | Official Git vocabulary ([git-revert](https://git-scm.com/docs/git-revert)) |
| **Version control** | A system that records every change to files so any earlier state can be recovered. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 19, "Version Control" (to verify against book) |

---

## 💻 Code Examples

### Example 1: Before, the decision computed twice

*File: [`projects/company-enricher/stages/03-change-safely/exercises/day11_before_refactor.py`](../projects/company-enricher/stages/03-change-safely/exercises/day11_before_refactor.py)*

```python
result = EnrichmentResult(
    company_name=company_name,
    status=self._decide(suggestion),
    reason=None if self._decide(suggestion) == ACCEPTED else WEAK_EVIDENCE,
    suggestion=suggestion,
    evidence_url=page.url,
    evidence_text=page.main_activity,
    checked_at=self._clock(),
)
```

### Example 2: After, one decision used twice

*File: [`projects/company-enricher/stages/03-change-safely/enricher/enricher.py`](../projects/company-enricher/stages/03-change-safely/enricher/enricher.py)*

```python
status = self._decide(suggestion)
result = EnrichmentResult(
    company_name=company_name,
    status=status,
    reason=None if status == ACCEPTED else WEAK_EVIDENCE,
    suggestion=suggestion,
    evidence_url=page.url,
    evidence_text=page.main_activity,
    checked_at=self._clock(),
)
```

**What's happening:** same fields, same values, same decisions.
The tests cannot tell the two versions apart, which is exactly the point.

### Example 3: The evidence that made it safe

*File: [`projects/company-enricher/stages/03-change-safely/tests/test_same_decisions.py`](../projects/company-enricher/stages/03-change-safely/tests/test_same_decisions.py)*

```python
@pytest.mark.parametrize("company, category", DECISIONS.items())
def test_decision_is_unchanged(enricher, company, category):
    result = enricher.enrich(company)
    assert (result.suggestion.category if result.status == ACCEPTED else None) == category
```

**What's happening:** twelve companies, including the missing website, each checked before and after every step.

### Example 4: The loop in Git

```bash
python -m pytest -q                      # green before you start
git commit -am "Compute the enrichment status once"
python -m pytest -q                      # red? undo the last commit:
git revert --no-edit HEAD
```

**What's happening:** each step is a commit, so undoing one is a command, not an archaeology project.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which change is a refactoring?**

- A. Storing the decision in a variable instead of computing it twice
- B. Raising the threshold from 0.82 to 0.85
- C. Sending missing websites to review instead of raising
- D. Adding a new category

<details>
<summary>Answer</summary>

**A.** Only this change keeps every observable behaviour the same. The others change what the service does.

</details>

**Q2. The tests turn red after a refactoring step and the cause is not obvious. What next?**

- A. Keep editing until they pass
- B. Revert to the last green commit and take a smaller step
- C. Delete the failing tests
- D. Commit anyway and fix later

<details>
<summary>Answer</summary>

**B.** A small step that fails is cheap to throw away. Debugging forward mixes the failed step with new edits.

</details>

**Q3. Why not refactor and change behaviour in the same commit?**

- A. Git does not allow it.
- B. It makes the commit message too long.
- C. When tests fail, you cannot tell which change caused it.
- D. Refactoring is slower.

<details>
<summary>Answer</summary>

**C.** Keeping them apart means a failing test points at one kind of change.

</details>

### Exercise 2 · Change: a refactoring sequence (⏱️ ~20 min)

**Goal:** Practise the loop on real code.

**Instructions:**
1. Work in a copy of `stages/03-change-safely` inside a Git repository.
2. Step 1: extract a method `_result_from(company_name, page, suggestion)` that builds the `EnrichmentResult`. Run the tests, then commit.
3. Step 2: move the `check_confidence` call inside `_result_from`. Run the tests, then commit.
4. Step 3: deliberately break something (change `>=` to `>` in `_decide`). Run the tests, watch which fail, then `git restore` the file.
5. Use `git log --oneline` to see your steps.

<details>
<summary>Hint</summary>

Step 3 should fail no characterization test, because no sample company scores exactly 0.82. Ask yourself what test would catch it, and add it.

</details>

### Exercise 3 · Transfer: pin before you change (⏱️ ~10 min)

Pick a function you have wanted to clean up.
Before touching it, write down which tests would tell you that its behaviour changed.
If none exist, write one characterization test first.

---

## 🔁 Module 3 · Before / After

**Before:** after Module 2 the structure was clear but fragile: one missing website stopped a whole batch, the clock and the website could not be controlled in tests, and only a handful of tests existed.

*File: [`projects/company-enricher/stages/02-control-complexity/tests/test_enricher.py`](../projects/company-enricher/stages/02-control-complexity/tests/test_enricher.py)*

```python
def test_unknown_company_raises_website_unavailable():
    with pytest.raises(WebsiteUnavailable):
        make_enricher().enrich("Ghost Gum Traders")
```

**After:** every failure has a designed meaning, the website and the clock sit behind injectable boundaries, a real HTTP adapter exists with a timeout, and 220 tests give evidence for every promise and decision.

*File: [`projects/company-enricher/stages/03-change-safely/tests/test_promises.py`](../projects/company-enricher/stages/03-change-safely/tests/test_promises.py)*

```python
def test_missing_website_needs_review_instead_of_crashing(enricher, store):
    result = enricher.enrich("Ghost Gum Traders")

    assert result.status == NEEDS_REVIEW
    assert result.reason == NO_WEBSITE
    assert store.saved_results == []
```

---

## 📖 Curated Resources

1. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topics 40, "Refactoring" and 19, "Version Control" (to verify against book).
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: when and how to restructure, and how to keep every step reversible.
2. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 16, "Modifying Existing Code" (to verify against book).
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: leaving the design better with each change.
3. **[Git documentation: git-revert](https://git-scm.com/docs/git-revert)**
   - Why: undoing a committed step safely.
4. **[Git documentation: git-restore](https://git-scm.com/docs/git-restore)**
   - Why: throwing away uncommitted edits.
5. **Free source:** the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), Topic 27, "Don't Outrun Your Headlights".
   - Why: the argument for small steps with feedback, free to read.

---

## 🤔 Reflection Questions

1. **Comprehension:** Why is "the tests still pass" the definition of a successful refactoring step?
2. **Application:** Which characterization test would you add to catch the `>=` to `>` change in Exercise 2?
3. **Connection:** How did Day 10's injectable clock make the characterization tests possible?
4. **Personal:** When did you last make a large change in one go? What would small steps have changed?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 12: Build language from examples](./day-12-language-from-examples.md). Module 4 begins: the code is safe to change, so now you make it speak the business's language.

**Before moving on, make sure you can:**

- [ ] Tell a refactoring from a behaviour change.
- [ ] Run the pin, step, test, commit loop.
- [ ] Undo a step with Git.

[← Previous: Day 10 Put volatile dependencies at boundaries](./day-10-volatile-dependencies.md) | [Course Home](../README.md) | [Next: Day 12 Build language from examples →](./day-12-language-from-examples.md)
