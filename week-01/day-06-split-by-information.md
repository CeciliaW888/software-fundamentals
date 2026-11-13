# Day 6: Split by information, not length

[← Previous: Day 5 Build deep modules](./day-05-deep-modules.md) | [Course Home](../README.md) | [Next: Day 7 Design it twice →](./day-07-design-it-twice.md)

> 📍 **Where we are in the story:** Week 1 · You can read the script now. Before it grows, you learn to tame its complexity.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Decide whether two pieces of code belong together by asking what knowledge they share.
2. Compare a short-function design with a deep-function design of the same classifier.
3. Recognise duplicated knowledge, not just duplicated text.
4. Explain orthogonality with an example from the Company Enricher.

**Plain idea:** keep code together when it shares knowledge, and apart when it does not, whatever the line count says.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 2 · Control complexity (lesson 0006)

---

## 📚 Core Concepts

### Observe: one classifier, two shapes

The project holds two versions of the same classifier, and a test proves they give identical answers for every sample company.

The first, in `exercises/day06_short_functions.py`, is split into six short functions: `tokenize`, `count_hits`, `total_hits`, `best_category`, `confidence_for`, and `suggest_category`.
Each one is two or three lines.

The second, `KeywordCategoryClassifier.suggest` in `classifier.py`, is one function of about ten lines.

Read both and ask a different question from "which is shorter?".
Ask: to change how confidence is calculated, how many functions must I read?
In the short version, confidence depends on `count_hits`, `total_hits`, and `confidence_for`, and the zero-hit rule sits in a fourth function.
In the deep version, all of that is on one screen.

### Say it plainly: split by what code knows

A rule that keeps showing up: code that shares knowledge should live together.
The six short functions all share one piece of knowledge, "a hit count per category decides the answer", so splitting them does not separate anything.
It only makes the reader jump between them and makes callers responsible for the order.

Now the opposite case.
The classifier knows nothing about websites, and the website module knows nothing about keywords.
That split is worth keeping: you can change one without reading the other.

Duplication follows the same rule.
In the Module 1 code, `predict_proba` returned probabilities in `CATEGORIES` order and `suggest` turned a position back into a name.
The text was not duplicated, but the knowledge "probabilities follow list order" was needed in two places.
The Module 2 classifier counts hits in a dictionary keyed by category, so no code has to know about positions at all.

### Name it: better together, DRY, orthogonality

John Ousterhout's *A Philosophy of Software Design*, Chapter 9, "Better Together Or Better Apart?" (to verify against book), argues that pieces of code should be combined when they share information, when combining simplifies the interface, or when it removes duplication.
He also warns against splitting a method only to make it shorter, because readers then have to understand several pieces at once.

*The Pragmatic Programmer* states the duplication rule as DRY in Topic 9, "DRY - The Evils of Duplication": each piece of knowledge in a system should be expressed in exactly one place that everything else defers to.
The authors stress that DRY is about knowledge and intent, not just copied text.

The same book's Topic 10, "Orthogonality" (to verify against book) describes the other half: two parts are orthogonal when changing one does not affect the other.
The classifier and the website module are orthogonal; the six short functions are not.

The publisher's free excerpt of Topic 9 makes the knowledge point in detail: the acid test for duplication is whether one change in the world forces edits in more than one place, and two pieces of code that merely look alike are not duplication if they could change for different reasons.
Ousterhout's free extract also contains section 9.8, his comparison with *Clean Code*: he agrees that very long functions are hard to read, but argues that splitting purely by length pushes readers to understand several functions at once.

> **Key Insight:** The right question is not "is this function too long?" but "what does this code know, and who else knows it?".

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **DRY** | Each piece of knowledge in a system should be expressed in exactly one authoritative place. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 9, "DRY - The Evils of Duplication", checked in the publisher's free excerpt |
| **Orthogonality** | Two parts are orthogonal when a change to one does not affect the other. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 10, "Orthogonality" (to verify against book) |
| **Duplicated knowledge** | The same fact or rule needed in more than one place, even if the code text differs. | Course-authored plain definition, following *The Pragmatic Programmer*'s DRY topic |
| **Shared information** | Knowledge two pieces of code must both have, which is a reason to keep them together. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 9 (to verify against book) |
| **Dictionary** | A Python mapping from keys to values, such as category to hit count. | Official Python vocabulary ([Python tutorial: dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)) |

---

## 💻 Code Examples

### Example 1: Six short functions

*File: [`projects/company-enricher/stages/02-control-complexity/exercises/day06_short_functions.py`](../projects/company-enricher/stages/02-control-complexity/exercises/day06_short_functions.py)*

```python
def total_hits(hits):
    return sum(hits.values())


def best_category(hits):
    return max(hits, key=hits.get)


def confidence_for(hits, category):
    return hits[category] / total_hits(hits)


def suggest_category(text):
    hits = count_hits(tokenize(text))
    if total_hits(hits) == 0:
        return OTHER, 0.0
    category = best_category(hits)
    return category, confidence_for(hits, category)
```

**What's happening:** each function is tiny, but to understand `suggest_category` you must read four others, and the zero-hit rule is separated from the confidence rule it protects.

### Example 2: One deep function

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/classifier.py`](../projects/company-enricher/stages/02-control-complexity/enricher/classifier.py)*

```python
class KeywordCategoryClassifier:
    """Suggests the category whose keywords appear most often.

    Confidence is the share of keyword hits that belong to the winning
    category. Text with no keywords is "Other" with confidence 0.0.
    """

    def suggest(self, text):
        words = re.findall(r"[a-z]+", text.lower())
        hits = {
            category: sum(1 for word in words if word in keywords)
            for category, keywords in CATEGORY_KEYWORDS.items()
        }
        total_hits = sum(hits.values())
        if total_hits == 0:
            return CategorySuggestion(OTHER, 0.0)
        best = max(hits, key=hits.get)
        return CategorySuggestion(best, hits[best] / total_hits)
```

**What's happening:** the whole rule, including the zero-hit case, reads top to bottom.
The docstring states the rule in one sentence, which is only possible because the rule lives in one place.

### Example 3: The test that keeps the comparison honest

*File: [`projects/company-enricher/stages/02-control-complexity/tests/test_designs_agree.py`](../projects/company-enricher/stages/02-control-complexity/tests/test_designs_agree.py)*

```python
@pytest.mark.parametrize("about", [page["about"] for page in SAMPLE_WEB.values()])
def test_both_designs_suggest_the_same_category(about):
    deep = KeywordCategoryClassifier().suggest(about)
    assert suggest_category(about) == (deep.category, deep.confidence)
```

**What's happening:** both designs are correct, so the choice between them is about who has to understand what, not about behaviour.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why does the Module 1 classifier break DRY even though no line is copied?**

- A. It uses two methods.
- B. Two methods both rely on the fact that probabilities follow `CATEGORIES` order.
- C. It has a docstring.
- D. It counts keywords.

<details>
<summary>Answer</summary>

**B.** DRY is about knowledge. The order rule is needed in both methods, so changing it means changing both.

</details>

**Q2. Which pair is orthogonal in the Module 2 code?**

- A. `total_hits` and `confidence_for`
- B. `CATEGORIES` and `CATEGORY_KEYWORDS`
- C. The classifier and the website module
- D. `best_category` and `suggest_category`

<details>
<summary>Answer</summary>

**C.** You can change how websites are read without touching keyword counting, and the reverse. The other pairs share knowledge.

</details>

**Q3. When is splitting a function a good idea?**

- A. When it is longer than ten lines
- B. When it has more than one `if`
- C. Always, because short functions are simpler
- D. When the parts use different knowledge and can be understood alone

<details>
<summary>Answer</summary>

**D.** A split pays off when each part can be read and changed on its own. Length alone is not a reason.

</details>

### Exercise 2 · Change: a new confidence rule (⏱️ ~15 min)

**Goal:** Feel the difference between the two designs.

**Instructions:**
1. New rule: when two categories tie for the most hits, confidence must be capped at 0.5.
2. Implement it in `exercises/day06_short_functions.py` and in `enricher/classifier.py`.
3. Count how many functions you had to read and edit in each.
4. Update `tests/test_designs_agree.py` only if your two versions disagree, then run `python -m pytest -q`.

<details>
<summary>Hint</summary>

In the deep version the tie check sits right after `best = ...`. In the short version you will need the hit counts, the total, and the best category at once, which no single short function has.

</details>

### Exercise 3 · Transfer: name the knowledge (⏱️ ~10 min)

Pick two modules in a codebase you know.
Write one sentence for what each one knows.
If the sentences overlap, write down the change that would have to touch both.

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 9, "Better Together Or Better Apart?" (to verify against book).
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: when to combine and when to separate code.
2. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topics 9, "DRY - The Evils of Duplication" and 10, "Orthogonality" (to verify against book).
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: duplication of knowledge and independent parts.
3. **[pytest: parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html)**
   - Why: how one test function in Example 3 runs once per sample company.
4. **Free sources:** the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) (Topic 9) and Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf) (section 9.8).
   - Why: both arguments in the authors' own words.

---

## 🤔 Reflection Questions

1. **Comprehension:** What knowledge do the six short functions all share?
2. **Application:** The business wants keyword weights, where "restaurant" counts double. Which module changes?
3. **Connection:** How does Day 5's deep module make the classifier and website code orthogonal?
4. **Critical Thinking:** Is there a length at which you would split the deep `suggest` anyway? What would justify it?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 7: Design it twice](./day-07-design-it-twice.md). You will design the service's public operation two ways and choose with criteria.

**Before moving on, make sure you can:**

- [ ] Explain DRY as a rule about knowledge.
- [ ] Give an orthogonal pair and a non-orthogonal pair from the project.
- [ ] Argue for or against a split without mentioning line counts.

[← Previous: Day 5 Build deep modules](./day-05-deep-modules.md) | [Course Home](../README.md) | [Next: Day 7 Design it twice →](./day-07-design-it-twice.md)
