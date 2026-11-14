# Day 4: Recognise complexity by its symptoms

[← Previous: Day 3 Follow the data and outside changes](./day-03-follow-the-data.md) | [Course Home](../README.md) | [Next: Day 5 Build deep modules →](./day-05-deep-modules.md)

> 📍 **Where we are in the story:** Week 1 · You can read the script now. Before it grows, you learn to tame its complexity.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Name the three symptoms of complexity: change amplification, cognitive load, and unknown unknowns.
2. Score one change request by how many places it touches and how much you must know.
3. Find the symptoms in the Module 1 code of the Company Enricher.
4. Show how moving knowledge into one place lowers the score.

**Plain idea:** complexity is whatever makes a change hard, and you can see it by trying one.

**Difficulty:** 🟢 Beginner\
**Estimated Time:** 30 minutes (15 reading + 15 hands-on)\
**Module:** 2 · Control complexity (lesson 0004)

---

## 📚 Core Concepts

### Observe: one small change request

The business asks for one new category: Agriculture, for farms and growers.
That sounds like a one-line job.
Try it on the Module 1 code in `stages/01-read-code/enricher.py` and count what you touch.

1. Add `"Agriculture"` to the `CATEGORIES` list.
2. Add an `"Agriculture"` entry to `CATEGORY_KEYWORDS`.
3. Put it in the right position, because `predict_proba` returns probabilities in `CATEGORIES` order and `suggest` turns a position back into a name.
4. Check the line `if confidence == 1 / len(CATEGORIES):`, which decides when the answer is "Other". It silently depends on how many categories exist.

Four places, and two of them need knowledge that the code does not state anywhere.
Now a second request: raise the confidence threshold from 0.82 to 0.85.
The number appears as the default in `select_confident_category_suggestions` and again inside `suggest_company_category`.
Miss one and the two functions disagree.

### Say it plainly: three ways code makes changes hard

Each problem you just hit has a different shape.

- **One change, many edits.** The threshold lives in two places, so one decision needs two edits.
- **Too much to hold in your head.** To add a category you must remember that a list's order and a dictionary's keys must agree.
- **Things you didn't know you needed to know.** Nothing near `CATEGORY_KEYWORDS` warns you about the `1 / len(CATEGORIES)` check.

The last one is the worst.
The first two slow you down; the third lets you ship a bug with confidence.

### Name it: the three symptoms

John Ousterhout's *A Philosophy of Software Design*, Chapter 2, "The Nature of Complexity", names these symptoms.
**Change amplification** is when a simple change needs edits in many places.
**Cognitive load** is how much a developer must know to complete a task.
**Unknown unknowns** are cases where it is not obvious which code must change, or what you need to know to change it.

He describes the causes as **dependencies** (code that cannot be understood or changed on its own) and **obscurity** (facts a reader needs but cannot see in the code).
The duplicated threshold is a dependency; the hidden `1 / len(CATEGORIES)` rule is obscurity.

*The Pragmatic Programmer* adds a warning about time in its Topic 3, "Software Entropy": small signs of neglect left unfixed invite more of the same, which the authors call "broken windows".
A second duplicated constant is easier to add once the first one is tolerated.

The fix in Module 2 is to put each piece of knowledge in exactly one place.
In `stages/02-control-complexity`, all category knowledge lives in `categories.py`, and the threshold is defined once.

The three symptoms are not only in Chapter 2: Ousterhout lists them again in his chapter on why to write comments, which is included in Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf).
*The Pragmatic Programmer*'s Topic 8, "The Essence of Good Design", offers one yardstick for every design choice.
Its Tip 14 (p. 28 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)) is "Good Design Is Easier to Change Than Bad Design", which is exactly what today's scoring measures.

> **Key Insight:** Count the edits and the facts a change needs. That count is a measure of complexity you can compare before and after.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Complexity** | Anything about the structure of a system that makes it hard to understand and modify. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2 |
| **Change amplification** | A simple change requiring edits in many different places. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2 |
| **Cognitive load** | How much a developer needs to know to complete a task. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2 |
| **Dependency** | Code that cannot be understood or modified in isolation from other code. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2 |
| **Obscurity** | Facts a reader needs to know that the code does not show. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2 |
| **Broken window** | A small, visible sign of neglect that, left unfixed, encourages more neglect. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 3, "Software Entropy" |

---

## 💻 Code Examples

### Example 1: Before, category knowledge in several places

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
class KeywordCategoryClassifier:
    def suggest(self, activity_summary):
        """Return the most likely category and its confidence."""
        probabilities = self.predict_proba([activity_summary])[0]
        confidence = max(probabilities)
        if confidence == 1 / len(CATEGORIES):
            return CategorySuggestion("Other", confidence)
        return CategorySuggestion(CATEGORIES[probabilities.index(confidence)], confidence)
```

**What's happening:** to read this you must know that probabilities come back in `CATEGORIES` order, that "Other" has no keywords, and that equal probabilities mean "no keywords found".
None of that is written down here.

### Example 2: After, one place for category knowledge

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/categories.py`](../projects/company-enricher/stages/02-control-complexity/enricher/categories.py)*

```python
OTHER = "Other"

CATEGORIES = [*CATEGORY_KEYWORDS, OTHER]

MINIMUM_CONFIDENCE = 0.82
```

**What's happening:** the category list is built from the keyword dictionary, so they cannot disagree.
The threshold has one definition that every other module imports.

### Example 3: A test that scores the change

*File: [`projects/company-enricher/stages/02-control-complexity/tests/test_enricher.py`](../projects/company-enricher/stages/02-control-complexity/tests/test_enricher.py)*

```python
def test_adding_a_category_is_one_edit(monkeypatch):
    from enricher import categories

    monkeypatch.setitem(categories.CATEGORY_KEYWORDS, "Agriculture", {"farm", "crops"})
    suggestion = KeywordCategoryClassifier().suggest("We farm crops")
    assert suggestion.category == "Agriculture"
```

**What's happening:** the test adds a category with one dictionary entry and checks that the classifier can suggest it.
If someone reintroduces a second place to edit, this test fails.

> **💡 Try it:** in `stages/01-read-code`, add Agriculture to `CATEGORY_KEYWORDS` only, then run `python -m pytest -q`. Which assumption breaks?

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. The threshold 0.82 appears in two functions. Which symptom is that?**

- A. Cognitive load
- B. Unknown unknowns
- C. Obscurity only
- D. Change amplification

<details>
<summary>Answer</summary>

**D.** One decision, the threshold, needs edits in two places: change amplification. It also adds some cognitive load, but the defining symptom is the extra edit.

</details>

**Q2. Why is the `1 / len(CATEGORIES)` check an unknown unknown?**

- A. Someone adding a category has no hint that this line depends on the count.
- B. It runs slowly on large lists.
- C. Python cannot divide by a list length.
- D. It is covered by a test.

<details>
<summary>Answer</summary>

**A.** The dependency is invisible from where you make the change, so you do not know you need to know it. Speed and syntax are not the problem.

</details>

**Q3. What makes adding a category cheaper in the Module 2 code?**

- A. Shorter variable names
- B. Category knowledge lives in one module and the list is derived from it
- C. More comments in every file
- D. Removing the Other category

<details>
<summary>Answer</summary>

**B.** Putting the knowledge in one place removes the extra edits and the hidden order rule. Comments and names help reading but do not remove edits.

</details>

### Exercise 2 · Change: score the change before and after (⏱️ ~15 min)

**Goal:** Measure complexity instead of arguing about it.

**Instructions:**
1. Make a two-column table: "Module 1 code" and "Module 2 code".
2. For the request "add Agriculture", count the files and lines you must edit in each version.
3. Count the facts you must know that are not written next to the code you edit.
4. Do the same for "change the threshold to 0.85".
5. Run the stage 02 tests to confirm the after-version works: `cd stages/02-control-complexity && python -m pytest -q`.

<details>
<summary>Hint</summary>

In stage 02, `categories.py` is the only file to edit for both requests. Search the stage for `0.82` to confirm it appears once.

</details>

### Exercise 3 · Transfer: find a broken window (⏱️ ~10 min)

Open any codebase you know.
Find one duplicated constant, one magic number, or one rule that lives in two places.
Write down the change request that would expose it and how many edits it would need.

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2, "The Nature of Complexity".
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: the source of the three symptoms and their two causes.
2. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 3, "Software Entropy".
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: why small neglected problems grow.
3. **[pytest: monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)**
   - Why: how Example 3 adds a category for one test only.
4. **Free source:** Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf).
   - Why: the comments chapter restates change amplification, cognitive load, and unknown unknowns in the author's own words.

---

## 🤔 Reflection Questions

1. **Comprehension:** Which of the three symptoms costs the most when it bites, and why?
2. **Application:** If the business later wants different thresholds per category, where would that knowledge live in the Module 2 code?
3. **Connection:** How did Day 3's hidden `SAMPLE_WEB` input create an unknown unknown?
4. **Critical Thinking:** Can putting everything in one file create a new kind of complexity?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 5: Build deep modules](./day-05-deep-modules.md). You will hide the website lookup behind one small interface.

**Before moving on, make sure you can:**

- [ ] Name the three symptoms and give a Company Enricher example of each.
- [ ] Score a change request by edits and required knowledge.
- [ ] Explain why a derived list cannot disagree with its source.

[← Previous: Day 3 Follow the data and outside changes](./day-03-follow-the-data.md) | [Course Home](../README.md) | [Next: Day 5 Build deep modules →](./day-05-deep-modules.md)
