# Day 12: Build language from examples

[← Previous: Day 11 Refactor under evidence](./day-11-refactor-under-evidence.md) | [Course Home](../README.md) | [Next: Day 13 Choose entities, values, and services deliberately →](./day-13-entities-values-services.md)

> 📍 **Where we are in the story:** Week 2 · The code is safe to change. Now you make it speak the business's language.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Collect concrete scenarios from the people who use the service before naming anything.
2. Spot a word that means different things to developers and to the business.
3. Turn agreed words into names in the code and tests.
4. Tell domain language apart from general programming vocabulary.

**Plain idea:** the business's own words, discovered through real examples, should be the names in the code.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 4 · Model the domain (lesson 0012)

---

## 📚 Core Concepts

### Observe: a word that means two things

The review team starts using the Module 3 output.
In the first week, a reviewer asks: "Why does it say *accepted* for Saltwater Kitchen? Nobody here accepted it."

In the code, `"accepted"` meant "confidence reached the threshold".
To the reviewers, *accepted* means a person looked at the evidence and agreed.
The same word described two different events, and the people who use the service were confused by the one written by the people who built it.

So instead of arguing about names, the team writes scenarios together, using real (made-up) companies:

| Scenario | What the reviewers say should happen |
|---|---|
| Saltwater Kitchen: "A seaside restaurant and cafe..." | The service **suggests** Food & Hospitality; nobody needs to look |
| Lantern Lane Bakery: bread, pastries, wholesale, baking | **Needs review**: the **evidence is weak**, it could be two categories |
| Ghost Gum Traders: no website found | **Needs review**: there is **no website** to use as evidence |
| Ironbark Fabrication, listed by a partner directory as Construction, but its page says it manufactures steel parts | **Needs review**: the **sources conflict** |

The last row is new.
Nobody had thought of it until a reviewer said "what if the partner directory disagrees?".
Examples found a rule that a discussion of names never would.

### Say it plainly: words first, then code

The process is simple.

1. Talk through concrete cases with the people who know the business.
2. Write down the words they use, and what each one means, in a short glossary.
3. Rename the code to use exactly those words.
4. Write the scenarios as tests, so the agreed language is checked on every run.

In stage 04, `"accepted"` becomes `Outcome.SUGGESTED`, review reasons become an enum, `ReviewReason`, with values for weak evidence, no website, and conflicting sources, and the scenario table above becomes `tests/test_scenarios.py`, almost row for row.

Not every word is domain language.
*Function*, *exception*, and *return value* are general programming vocabulary; reviewers never say them.
*Suggested*, *needs review*, and *weak evidence* belong to this business and this team.

### Name it: ubiquitous language, knowledge crunching

Eric Evans's *Domain-Driven Design*, Chapter 1, "Crunching Knowledge", describes developers and domain experts working through examples together until a useful model emerges.
Chapter 2, "Communication and the Use of Language", introduces the **ubiquitous language**: a language built around the domain model and used consistently by the team in conversation, documents, and code.
Chapter 3, "Binding Model and Implementation", argues that the code should follow the model closely, so a change in the language is a change in the code.

Ubiquitous language is specific to one domain and one team.
It is not a name for general programming vocabulary.

Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/), a summary of the book's patterns, describes the ubiquitous language as a shared team language used in conversation, diagrams, documents, and code, changed deliberately whenever the model changes.
*The Pragmatic Programmer* reaches a similar practice from the requirements side; in the publisher's [official list of the book's tips](https://pragprog.com/tips/), Tip 77 (p. 246) is "Requirements Are Learned in a Feedback Loop" and Tip 80 (p. 251) is "Use a Project Glossary".

> **Key Insight:** If the people who use the software would not say a word, it probably should not name a business concept in the code.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Domain** | The subject area in which the software is used and the knowledge needed to work in that area. | Paraphrased from Eric Evans, *Domain-Driven Design* |
| **Domain expert** | A person who knows the business area well, such as a reviewer who categorises companies. | Standard DDD vocabulary; this plain definition is course-authored |
| **Ubiquitous language** | Language built around one domain model and used consistently by the team in speech, documents, and code. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 2 |
| **Knowledge crunching** | Working through examples with domain experts to distil a useful model. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 1 |
| **Scenario** | A concrete example of a situation and what should happen in it. | Course-authored plain definition |
| **Enum** | A Python type with a fixed set of named values, such as `Outcome.SUGGESTED`. | Official Python vocabulary ([enum](https://docs.python.org/3/library/enum.html)) |

---

## 💻 Code Examples

### Example 1: The agreed words, as code

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/core/model.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/core/model.py)*

```python
class Outcome(Enum):
    SUGGESTED = "suggested"
    NEEDS_REVIEW = "needs_review"


class ReviewReason(Enum):
    WEAK_EVIDENCE = "weak_evidence"
    NO_WEBSITE = "no_website"
    CONFLICTING_SOURCES = "conflicting_sources"
```

**What's happening:** the outcome and every reason a person might need to look are a fixed set of names.
A typo such as `"neds_review"` is now an error instead of a silent new status.

### Example 2: The scenarios, as tests

*File: [`projects/company-enricher/stages/04-model-the-domain/tests/test_scenarios.py`](../projects/company-enricher/stages/04-model-the-domain/tests/test_scenarios.py)*

```python
SCENARIOS = [
    ("Saltwater Kitchen", None, Outcome.SUGGESTED, None),
    ("Lantern Lane Bakery", None, Outcome.NEEDS_REVIEW, ReviewReason.WEAK_EVIDENCE),
    ("Ghost Gum Traders", None, Outcome.NEEDS_REVIEW, ReviewReason.NO_WEBSITE),
    ("Ironbark Fabrication", Category.CONSTRUCTION, Outcome.NEEDS_REVIEW, ReviewReason.CONFLICTING_SOURCES),
    ("Ironbark Fabrication", Category.MANUFACTURING, Outcome.SUGGESTED, None),
]


@pytest.mark.parametrize("name, hint, outcome, reason", SCENARIOS)
def test_scenario(enricher, name, hint, outcome, reason):
    result = enricher.enrich(company(name, hint))
    assert (result.outcome, result.reason) == (outcome, reason)
```

**What's happening:** a reviewer can read the `SCENARIOS` list and check it against what they said.
The second column is the partner directory's hint, which Day 14 explains.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why was `"accepted"` renamed?**

- A. It was too long.
- B. Python reserves the word.
- C. The tests required it.
- D. To reviewers it meant a person had agreed, which the code never checked.

<details>
<summary>Answer</summary>

**D.** The code used a business word for a different event. Renaming to `SUGGESTED` makes the code say what actually happened.

</details>

**Q2. Which of these is domain language for this service?**

- A. Weak evidence
- B. Exception
- C. Return value
- D. Function

<details>
<summary>Answer</summary>

**A.** Reviewers say "weak evidence". The others are general programming vocabulary, not this business's language.

</details>

**Q3. How did the team discover the conflicting-sources rule?**

- A. From a code review
- B. By walking through a concrete example with reviewers
- C. From a performance test
- D. From the Python documentation

<details>
<summary>Answer</summary>

**B.** A concrete case, a partner listing that disagrees with the website, revealed a rule nobody had named.

</details>

### Exercise 2 · Change: add a scenario (⏱️ ~15 min)

**Goal:** Grow the language through an example.

**Instructions:**
1. Reviewers say: "If a company's About page is in another language and no keywords match, we call that *unreadable*."
2. Decide whether *unreadable* is a new `ReviewReason` or the same as weak evidence. Write one sentence on how you decided.
3. If it is new, add it to `ReviewReason`, add a scenario row, and make it pass.
4. Run `python -m pytest -q` in `stages/04-model-the-domain`.

<details>
<summary>Hint</summary>

Ask the reviewers' question: would they act differently on an unreadable page than on weak evidence? If yes, it deserves its own word.

</details>

### Exercise 3 · Transfer: find a word that means two things (⏱️ ~10 min)

In a project you know, find a business word that developers and users understand differently.
Write both meanings and one concrete example that shows the difference.

---

## 📖 Curated Resources

1. **Domain reading:** Eric Evans, *Domain-Driven Design*, Chapters 1 to 3: "Crunching Knowledge", "Communication and the Use of Language", and "Binding Model and Implementation".
   - 🔗 [DDD resources from Domain Language](https://www.domainlanguage.com/ddd/)
   - Why: the source of ubiquitous language and model-driven code.
2. **[Python documentation: enum](https://docs.python.org/3/library/enum.html)**
   - Why: how `Outcome` and `ReviewReason` work.
3. **[pytest: parametrizing tests](https://docs.pytest.org/en/stable/how-to/parametrize.html)**
   - Why: how one scenario table becomes five tests.
4. **Free source:** Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/).
   - Why: the author's own short definitions of ubiquitous language and the other patterns in this module, free to read.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is the difference between domain language and programming vocabulary?
2. **Application:** Which other names in stage 04 would you check with the reviewers?
3. **Connection:** How does Day 1's advice on names apply to business words?
4. **Critical Thinking:** What happens to a ubiquitous language when two teams use the same word differently? (Day 14 returns to this.)

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 13: Choose entities, values, and services deliberately](./day-13-entities-values-services.md). You will give the agreed words the right shape in code.

**Before moving on, make sure you can:**

- [ ] Collect scenarios before naming things.
- [ ] Explain why `"accepted"` became `SUGGESTED`.
- [ ] Keep domain words and programming words apart.

[← Previous: Day 11 Refactor under evidence](./day-11-refactor-under-evidence.md) | [Course Home](../README.md) | [Next: Day 13 Choose entities, values, and services deliberately →](./day-13-entities-values-services.md)
