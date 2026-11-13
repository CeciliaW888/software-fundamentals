# Day 14: Protect context boundaries

[← Previous: Day 13 Choose entities, values, and services deliberately](./day-13-entities-values-services.md) | [Course Home](../README.md) | [Next: Day 15 Distil the core →](./day-15-distil-the-core.md)

> 📍 **Where we are in the story:** Week 2 · The code is safe to change. Now you make it speak the business's language.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Recognise when another system's data comes with its own model and words.
2. Draw a simple context map of the Company Enricher and its neighbours.
3. Translate a partner's records into your own model in one adapter.
4. Decide what to do with partner values your model has no word for.

**Plain idea:** when another system speaks a different language, translate at the border instead of letting its words spread through your code.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 4 · Model the domain (lesson 0014)

---

## 📚 Core Concepts

### Observe: a partner's data arrives

A made-up partner, the Tradeline Directory, offers a feed of business listings.
Each listing looks like this:

| Field | Example | What it means to Tradeline |
|---|---|---|
| `listing_id` | `TL-0042` | Tradeline's own ID |
| `trading_name` | `Saltwater Kitchen Pty Ltd` | The legal trading name, with suffix |
| `sector_code` | `HSP` | Tradeline's three-letter sector code |

None of these match the Company Enricher's words.
Tradeline says *listing*, we say *company*.
Tradeline has *sector codes*, we have *categories*.
Its names include "Pty Ltd", which our website lookup does not expect.

The tempting shortcut is to pass the listing dictionary straight into the core and add `if listing["sector_code"] == "HSP"` wherever needed.
Within a month, Tradeline's codes would be scattered through the policy, the tests, and the reports, and a change on their side would break code everywhere.

### Say it plainly: translate once, at the border

Stage 04 adds one module, `adapters/partner_directory.py`, with one job: turn a Tradeline listing into our `Company`.

- `listing_id` becomes our `company_id`, prefixed `tradeline:` so it cannot clash with IDs from elsewhere.
- `trading_name` loses its legal suffix and becomes `name`.
- `sector_code` is mapped through a table to one of our `Category` values, which becomes the company's `directory_hint`.
- A code we have no mapping for becomes "no hint", never a guess.

After the translation, the core sees only `Company` and `Category`.
The partner's vocabulary stops at the adapter, and Day 13's `SuggestionPolicy` can use the hint in our own terms: if the directory and the website disagree, the company needs review for conflicting sources.

A simple **context map** shows who speaks which language:

| Context | Its language | Relationship to the Company Enricher |
|---|---|---|
| Company Enricher (ours) | company, category, suggestion, needs review | the core |
| Company websites | URLs, HTML, About pages | outside; reached through the website adapter |
| Tradeline Directory | listing, trading name, sector code | partner; translated by the anticorruption layer |
| Review team | the same language as ours | downstream: works from our results |

### Name it: bounded context, context map, anticorruption layer

Eric Evans's *Domain-Driven Design*, Chapter 14, "Maintaining Model Integrity" (to verify against book), explains that a model is only consistent within a boundary.
A **bounded context** is the explicit boundary within which one model and its language apply.
A **context map** shows the bounded contexts in play and how they relate.
An **anticorruption layer** is an isolating layer that translates between your model and another system's, so the other model cannot corrupt yours.

The translation table is a model decision, not plumbing.
Mapping `ICT` to Software & IT is a claim the reviewers should agree with, which is why it lives in one readable place.

Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) describes an anticorruption layer as an isolating layer that gives your code the other system's functionality in terms of your own model, and talks to the other system through the interface it already has.
That is `company_from_listing`: Tradeline keeps its feed, and we keep our words.

> **Key Insight:** Every external model you let in unchanged becomes part of your model. Translate it at the border, in one place.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Bounded context** | The explicit boundary within which one model and its language apply. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 14 (to verify against book) |
| **Context map** | A description of the bounded contexts in play and how they relate. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 14 (to verify against book) |
| **Anticorruption layer** | A layer that translates between your model and another system's, keeping the other model out. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 14 (to verify against book) |
| **Directory hint** | The category a partner directory suggests for a company, translated into our categories. | Course domain term |
| **Translation table** | An explicit mapping from another system's values to yours. | Course-authored plain definition |

---

## 💻 Code Examples

### Example 1: The translation table

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/adapters/partner_directory.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/adapters/partner_directory.py)*

```python
SECTOR_CODE_TO_CATEGORY = {
    "RTL": Category.RETAIL,
    "WHS": Category.WHOLESALE,
    "MFG": Category.MANUFACTURING,
    "ICT": Category.SOFTWARE,
    "HLT": Category.HEALTHCARE,
    "HSP": Category.FOOD,
    "CON": Category.CONSTRUCTION,
    "FIN": Category.FINANCE,
    "EDU": Category.EDUCATION,
}
```

**What's happening:** the only place in the service where Tradeline's sector codes appear.

### Example 2: The anticorruption layer

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/adapters/partner_directory.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/adapters/partner_directory.py)*

```python
def company_from_listing(listing):
    """Translate one Tradeline listing into a Company.

    Unknown sector codes become "no hint", never a guessed category.
    """
    name = listing["trading_name"]
    for suffix in LEGAL_SUFFIXES:
        name = name.removesuffix(suffix)
    return Company(
        company_id=f"tradeline:{listing['listing_id']}",
        name=name,
        directory_hint=SECTOR_CODE_TO_CATEGORY.get(listing.get("sector_code")),
    )
```

**What's happening:** input in Tradeline's words, output in ours.
Nothing after this function knows Tradeline exists.

### Example 3: Testing the translation

*File: [`projects/company-enricher/stages/04-model-the-domain/tests/test_partner_directory.py`](../projects/company-enricher/stages/04-model-the-domain/tests/test_partner_directory.py)*

```python
def test_unknown_sector_code_gives_no_hint():
    listing = {"listing_id": "TL-0099", "trading_name": "Quiet Hours Studio", "sector_code": "ZZZ"}
    assert company_from_listing(listing).directory_hint is None
```

**What's happening:** the safest translation of an unknown value is "we don't know", which the policy treats as no hint.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. What is wrong with passing Tradeline listings straight into the core?**

- A. Dictionaries are slow.
- B. Tradeline's codes and names would spread through the core, so their changes break our code.
- C. Python cannot pass dictionaries.
- D. It needs a database.

<details>
<summary>Answer</summary>

**B.** Letting another model in unchanged makes it part of yours. The anticorruption layer keeps it at the border.

</details>

**Q2. A listing arrives with sector code `ZZZ`. What should the adapter do?**

- A. Guess the closest category
- B. Raise an exception and stop the import
- C. Return a company with no directory hint
- D. Use Other as the hint

<details>
<summary>Answer</summary>

**C.** An unknown code means "no information". Guessing, or using Other, would invent a claim the partner never made.

</details>

**Q3. In the context map, how does the review team relate to the Company Enricher?**

- A. It is upstream and supplies data.
- B. It is translated by the anticorruption layer.
- C. It has no relationship.
- D. It is downstream and works from our results, in our language.

<details>
<summary>Answer</summary>

**D.** Reviewers consume our results and share our language, so no translation is needed between them and us.

</details>

### Exercise 2 · Change: the partner changes its feed (⏱️ ~15 min)

**Goal:** See the anticorruption layer absorb a change.

**Instructions:**
1. Tradeline renames `trading_name` to `business_name` and adds a new code `AGR` for agriculture.
2. Update `company_from_listing` so it accepts the new field name.
3. Decide what `AGR` should map to, given our category list, and write down why.
4. Add a test for each change, then run `python -m pytest -q` and confirm no file outside `adapters/` changed.

<details>
<summary>Hint</summary>

We have no Agriculture category, so `AGR` maps to no hint until the business adds one. Day 4 showed that adding a category is one edit.

</details>

**Optional exercise: swap in a real taxonomy (e.g. ANZSIC or NAICS) behind an adapter, so the core keeps its own plain category list.**
Write a second translation table from a published industry classification to our `Category` values, and test it the same way.

### Exercise 3 · Transfer: draw a context map (⏱️ ~10 min)

For a system you know, list every outside system it exchanges data with.
For each, write two of its words that differ from yours, and where the translation happens today.

---

## 📖 Curated Resources

1. **Domain reading:** Eric Evans, *Domain-Driven Design*, Chapter 14, "Maintaining Model Integrity" (to verify against book).
   - 🔗 [DDD resources from Domain Language](https://www.domainlanguage.com/ddd/)
   - Why: bounded contexts, context maps, and the anticorruption layer.
2. **[Python documentation: str.removesuffix](https://docs.python.org/3/library/stdtypes.html#str.removesuffix)**
   - Why: how the adapter strips "Pty Ltd" safely.
3. **[Python documentation: dict.get](https://docs.python.org/3/library/stdtypes.html#dict.get)**
   - Why: how an unknown sector code becomes `None` instead of an error.
4. **Free source:** Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/).
   - Why: short definitions of bounded context, context map, and anticorruption layer.

---

## 🤔 Reflection Questions

1. **Comprehension:** What does the anticorruption layer protect, and from what?
2. **Application:** A second directory arrives with different codes. Where does its translation go?
3. **Connection:** How is this adapter like Day 10's HTTP adapter, and how is it different?
4. **Critical Thinking:** When might a translation layer cost more than it saves?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 15: Distil the core](./day-15-distil-the-core.md). You will decide which part of the service deserves the most design care.

**Before moving on, make sure you can:**

- [ ] Draw a context map for the Company Enricher.
- [ ] Explain what `company_from_listing` translates.
- [ ] Handle a partner value your model has no word for.

[← Previous: Day 13 Choose entities, values, and services deliberately](./day-13-entities-values-services.md) | [Course Home](../README.md) | [Next: Day 15 Distil the core →](./day-15-distil-the-core.md)
