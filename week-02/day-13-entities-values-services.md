# Day 13: Choose entities, values, and services deliberately

[← Previous: Day 12 Build language from examples](./day-12-language-from-examples.md) | [Course Home](../README.md) | [Next: Day 14 Protect context boundaries →](./day-14-context-boundaries.md)

> 📍 **Where we are in the story:** Week 2 · The code is safe to change. Now you make it speak the business's language.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Decide whether a concept is defined by its identity or by its values.
2. Make a value object that refuses impossible values.
3. Give an entity an identity that survives a change of name.
4. Put a rule that belongs to no single object in a domain service.

**Plain idea:** some things are "the same one" over time, some things are just their values, and some rules belong to neither.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 4 · Model the domain (lesson 0013)

---

## 📚 Core Concepts

### Observe: three questions about three concepts

Take three concepts from the Day 12 language and ask the same questions of each.

**A confidence of 0.6.** Is one 0.6 different from another 0.6? No; they are interchangeable. Can a confidence change? It shouldn't; a new estimate is a new value. Can it be 1.7? Never.

**A company.** Saltwater Kitchen renames itself Saltwater Kitchen & Bar. Is it the same company? Yes; its history, its suggestions, and its reviews all still belong to it. Two different companies called "Northgate Builders" in two states? Different companies, same name.

**The rule "suggest only when confident and not contradicted by the partner directory".** Does it belong to the suggestion? It needs the company's directory hint. To the company? It needs the suggestion's confidence. It belongs to neither.

### Say it plainly: three shapes for three kinds of concept

The answers point to three shapes.

- **Things defined by their values** are compared by value and never change. In stage 04: `Confidence`, `Evidence`, and `CategorySuggestion`, all frozen dataclasses. `Confidence` also checks itself: creating `Confidence(1.7)` raises `ValueError`, so an impossible confidence cannot exist anywhere in the service. That replaces Day 8's separate `check_confidence` call; the rule now lives where the value is made.
- **Things defined by their identity** have an ID that stays the same while other attributes change. `Company` compares equal by `company_id` only, so a renamed company is still the same company, and two companies with the same name are not.
- **Rules that involve several objects** go in a separate object named for the rule. `SuggestionPolicy.decide(suggestion, company)` holds the confidence threshold and the conflicting-sources rule.

The category list itself is an enum, `Category`, because the business agreed on a fixed list.

Not everything needs one of these shapes.
The keyword classifier is still a plain class with one method; giving it identity or value semantics would add nothing.

### Name it: value objects, entities, domain services

Eric Evans's *Domain-Driven Design*, Chapter 5, "A Model Expressed in Software", names these shapes.
An **entity** is an object defined by a thread of continuity and identity rather than by its attributes.
A **value object** describes something and has no conceptual identity; it is often best made immutable.
A **service** is an operation that stands alone in the model because it does not belong naturally to any entity or value object.

Chapter 4, "Isolating the Domain", explains why these objects live in their own layer, away from storage and user interface code.
Chapter 6, "The Life Cycle of a Domain Object", discusses keeping such objects consistent; Day 20 uses its idea of an aggregate.

Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) gives the same three shapes in brief, and adds a warning that fits the two companies called Northgate Builders: mistaken identity between entities can corrupt data.

> **Key Insight:** Ask "is this the same one, or just the same value?" before choosing a shape. The answer decides equality, mutability, and where rules live.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Entity** | An object defined by its identity and continuity over time, not by its attributes. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 5 |
| **Value object** | An object that describes something, has no identity of its own, and is usually immutable. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 5 |
| **Domain service** | An operation in the model that does not belong naturally to any entity or value object. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 5 |
| **Immutable** | Unable to change after it is created. | Standard software vocabulary; Python's [frozen dataclasses](https://docs.python.org/3/library/dataclasses.html#frozen-instances) provide it |
| **Identity** | What makes an entity the same one over time; here, `company_id`. | Course-authored plain definition |
| **Invariant** | A rule that must always be true, such as "confidence is between 0 and 1". | Standard software vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: A value object that guards its own rule

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/core/model.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/core/model.py)*

```python
@dataclass(frozen=True)
class Confidence:
    value: float

    def __post_init__(self):
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"confidence must be between 0 and 1, got {self.value!r}")

    def at_least(self, minimum):
        return self.value >= minimum
```

**What's happening:** the check runs every time a `Confidence` is created, so no code anywhere can hold an impossible one.

### Example 2: An entity equal by identity

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/core/model.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/core/model.py)*

```python
@dataclass(eq=False)
class Company:
    company_id: str
    name: str
    directory_hint: Category | None = field(default=None)

    def __eq__(self, other):
        return isinstance(other, Company) and other.company_id == self.company_id

    def __hash__(self):
        return hash(self.company_id)
```

**What's happening:** `eq=False` stops the dataclass from comparing every field; the explicit `__eq__` compares only the identity.

### Example 3: A rule that belongs to no single object

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/core/policy.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/core/policy.py)*

```python
def decide(self, suggestion, company):
    """Return (Outcome, ReviewReason or None)."""
    if not suggestion.confidence.at_least(self._minimum_confidence):
        return Outcome.NEEDS_REVIEW, ReviewReason.WEAK_EVIDENCE
    if company.directory_hint and company.directory_hint != suggestion.category:
        return Outcome.NEEDS_REVIEW, ReviewReason.CONFLICTING_SOURCES
    return Outcome.SUGGESTED, None
```

**What's happening:** the policy reads like the reviewers' rule, and it is the only place the threshold is used.

### Example 4: Tests in the business's terms

*File: [`projects/company-enricher/stages/04-model-the-domain/tests/test_model.py`](../projects/company-enricher/stages/04-model-the-domain/tests/test_model.py)*

```python
def test_company_keeps_its_identity_when_renamed():
    before = Company(company_id="tradeline:TL-0042", name="Saltwater Kitchen")
    after = Company(company_id="tradeline:TL-0042", name="Saltwater Kitchen & Bar")
    assert before == after
    assert Company("a", "Same Name") != Company("b", "Same Name")
```

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which concept should be a value object?**

- A. A company
- B. A reviewer's account
- C. A piece of evidence: a URL and an excerpt
- D. A batch run with its own history

<details>
<summary>Answer</summary>

**C.** Two pieces of evidence with the same URL and excerpt are interchangeable. The others have identities that persist over time.

</details>

**Q2. Two `Company` objects have the same name but different IDs. Are they equal?**

- A. Yes, because names match
- B. Only if they have the same directory hint
- C. Python cannot compare them
- D. No, because identity is the company ID

<details>
<summary>Answer</summary>

**D.** Entities are equal by identity, so two different companies with one name stay distinct.

</details>

**Q3. Why is `SuggestionPolicy` a service rather than a method on `Company`?**

- A. The rule needs both a suggestion and a company, and belongs naturally to neither.
- B. Services run faster.
- C. Companies cannot have methods.
- D. Evans forbids methods on entities.

<details>
<summary>Answer</summary>

**A.** A rule spanning several objects reads more clearly as its own named operation.

</details>

### Exercise 2 · Change: a new value object (⏱️ ~20 min)

**Goal:** Give a concept the right shape.

**Instructions:**
1. Reviewers want evidence excerpts limited to 200 characters, and never empty.
2. Make `Evidence` enforce both rules in `__post_init__`, as `Confidence` does.
3. Write two tests in `tests/test_model.py`: one for an empty excerpt, one for a too-long excerpt.
4. Run `python -m pytest -q` and check that every scenario still passes.

<details>
<summary>Hint</summary>

Check `len(self.excerpt)` and `self.excerpt.strip()`. All sample first sentences are well under 200 characters.

</details>

### Exercise 3 · Transfer: identity or value? (⏱️ ~10 min)

List five concepts from a system you know.
For each, answer: "is it the same one over time, or just its values?".
Find one that is modelled the wrong way round.

---

## 📖 Curated Resources

1. **Domain reading:** Eric Evans, *Domain-Driven Design*, Chapter 5, "A Model Expressed in Software", with Chapters 4 and 6 for context.
   - 🔗 [DDD resources from Domain Language](https://www.domainlanguage.com/ddd/)
   - Why: the source of entities, value objects, and services.
2. **[Python documentation: dataclasses](https://docs.python.org/3/library/dataclasses.html)**
   - Why: `frozen=True`, `eq=False`, and `__post_init__`.
3. **[Python documentation: object.__hash__](https://docs.python.org/3/reference/datamodel.html#object.__hash__)**
   - Why: why an object that defines `__eq__` should also define `__hash__`.
4. **Free source:** Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/).
   - Why: short definitions of entities, value objects, and services.

---

## 🤔 Reflection Questions

1. **Comprehension:** Why are value objects usually immutable?
2. **Application:** Is a category suggestion an entity or a value? What would change if reviewers could comment on one?
3. **Connection:** How does `Confidence` move Day 8's crash-early check closer to the data?
4. **Critical Thinking:** When would modelling everything as entities, values, and services be overengineering?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 14: Protect context boundaries](./day-14-context-boundaries.md). A partner's data arrives with its own model; you keep it out of yours.

**Before moving on, make sure you can:**

- [ ] Tell an entity from a value object with one question.
- [ ] Write a value object that rejects impossible values.
- [ ] Explain when a rule deserves its own domain service.

[← Previous: Day 12 Build language from examples](./day-12-language-from-examples.md) | [Course Home](../README.md) | [Next: Day 14 Protect context boundaries →](./day-14-context-boundaries.md)
