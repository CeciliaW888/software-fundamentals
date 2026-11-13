# Day 15: Distil the core

[← Previous: Day 14 Protect context boundaries](./day-14-context-boundaries.md) | [Course Home](../README.md) | [Next: Day 16 Turn qualities into measurable requirements →](../week-03/day-16-measurable-requirements.md)

> 📍 **Where we are in the story:** Week 2 · The code is safe to change. Now you make it speak the business's language.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Separate the parts of the service that make it valuable from the parts any system needs.
2. Write a one-paragraph statement of what the core does.
3. Organise the code so the core can be read on its own.
4. Enforce the separation with a test.

**Plain idea:** spend your best design effort on the small part that makes this service worth having, and keep everything else out of its way.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 4 · Model the domain (lesson 0015)

---

## 📚 Core Concepts

### Observe: which parts make the service valuable?

List everything the Company Enricher does and ask, for each part: could we buy this, copy it, or use a library?

| Part | Could we get it elsewhere? | Kind |
|---|---|---|
| Deciding when a suggestion can skip review, and why | No: it is our reviewers' judgement, written as rules | **core** |
| The category list, keywords, and evidence | No: agreed with our reviewers | **core** |
| Translating the Tradeline Directory | Partly: needed only because of our partner | **supporting** |
| Fetching web pages and stripping HTML | Yes: standard libraries do it | **generic** |
| Keeping results in memory or a database | Yes: any database | **generic** |

The core is small: a few rules about evidence, confidence, and conflicting sources.
Everything else exists to feed it or store what it decides.

### Say it plainly: give the core its own room

Stage 04 makes that split visible in the folder structure.

- `enricher/core/` holds categories, the model, the classifier, the policy, the enrich operation, and the `ports.py` file that says what the core needs from outside.
- `enricher/adapters/` holds the website sources, the partner directory, and the store.

A new developer can read `core/` alone and understand what the service decides and why, without seeing a URL, an HTML tag, or a partner code.
The package docstring states the purpose in one paragraph, a short **domain vision statement**:

> The Company Enricher suggests a business category for a company from its own website, keeps the evidence, and sends any case a person should judge to review: weak evidence, no website, or sources that disagree.

A test, `test_layers.py`, reads every file in `core/` and fails if any of them imports from `adapters/`.
The separation is no longer a convention someone might forget; it is checked on every run.

### Name it: core domain, generic subdomains, segregated core

Eric Evans's *Domain-Driven Design*, Chapter 15, "Distillation" (to verify against book), describes distilling a model to find the **core domain**: the part that is most valuable and specialised, and that deserves the best people and the most care.
**Generic subdomains** are parts that are needed but not special to the business, and can be handled with off-the-shelf solutions or less effort.
The chapter also describes a **domain vision statement**, a short description of the core's value, and a **segregated core**, where the core's code is separated from supporting code so it can be understood on its own.

Ousterhout reaches the same conclusion from the design side in Chapter 21, "Decide What Matters", checked in Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf).
He argues that good design separates what matters from what doesn't, structures the system around what matters, and keeps everything else out of its way.
The `core/` folder and `test_layers.py` are that idea applied to the Company Enricher.

> **Key Insight:** If you can't point at the folder that holds your business's reason to exist, nobody can protect it.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Core domain** | The most valuable and specialised part of the model, where design effort should go first. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 15 (to verify against book) |
| **Generic subdomain** | A part the system needs that is not special to this business. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 15 (to verify against book) |
| **Supporting subdomain** | A part specific to this business that exists to support the core. | Standard DDD vocabulary; this plain definition is course-authored |
| **Domain vision statement** | A short description of the core domain and the value it brings. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 15 (to verify against book) |
| **Segregated core** | Core code separated from supporting code so it can be understood alone. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 15 (to verify against book) |
| **Port** | A small interface in the core that says what it needs from the outside world. | Standard software vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: The core's needs, in the core's words

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/core/ports.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/core/ports.py)*

```python
class WebsiteSource(Protocol):
    def about_page(self, company_name: str) -> AboutPage:
        """Return the company's About page or raise WebsiteUnavailable."""


class ResultStore(Protocol):
    def save(self, result) -> None:
        """Keep a suggested result."""
```

**What's happening:** the core declares what it needs; adapters provide it.
The arrows of dependency point inwards, towards the core.

### Example 2: The enrich operation, core only

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/core/enrich.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/core/enrich.py)*

```python
suggestion = self._classifier.suggest(page.main_activity)
outcome, reason = self._policy.decide(suggestion, company)
```

**What's happening:** two lines of business logic: classify the evidence, then let the policy decide.
Everything around them in `enrich` is gathering evidence and recording the result.

### Example 3: The separation, enforced

*File: [`projects/company-enricher/stages/04-model-the-domain/tests/test_layers.py`](../projects/company-enricher/stages/04-model-the-domain/tests/test_layers.py)*

```python
def test_core_does_not_import_adapters():
    offenders = {
        path.name: module
        for path in CORE.glob("*.py")
        for module in imported_modules(path)
        if module.startswith("enricher.adapters")
    }
    assert offenders == {}
```

**What's happening:** if anyone imports an adapter into the core, the failure names the file and the import.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which part of the Company Enricher is the core domain?**

- A. The rules for when a suggestion needs review
- B. Fetching HTML pages
- C. Saving results
- D. Logging

<details>
<summary>Answer</summary>

**A.** The review rules encode the business's own judgement. The others are generic and could come from libraries.

</details>

**Q2. Why does the core declare `WebsiteSource` instead of importing `HttpWebsiteSource`?**

- A. Because Protocols are faster
- B. To make the core's dependencies point inwards, so adapters can change freely
- C. Because HTTP is not allowed in Python
- D. To avoid writing tests

<details>
<summary>Answer</summary>

**B.** The core states what it needs; any adapter can provide it. The core never changes when an adapter does.

</details>

**Q3. What does `test_layers.py` protect?**

- A. Performance of the core
- B. The spelling of category names
- C. The rule that the core never imports adapters
- D. The partner's sector codes

<details>
<summary>Answer</summary>

**C.** It turns the folder convention into a check that fails on every run if broken.

</details>

### Exercise 2 · Change: break and restore the boundary (⏱️ ~15 min)

**Goal:** See the guard work.

**Instructions:**
1. In `stages/04-model-the-domain/enricher/core/enrich.py`, add `from enricher.adapters.store import InMemoryResultStore` and use it as a default store.
2. Run `python -m pytest -q`. Read the failure message.
3. Undo the change with `git restore` or by hand.
4. Write your own one-paragraph domain vision statement for the service, and compare it with the one above.

<details>
<summary>Hint</summary>

The failure lists `{'enrich.py': 'enricher.adapters.store'}`, pointing straight at the bad import.

</details>

### Exercise 3 · Transfer: find your core (⏱️ ~10 min)

For a system you know, write its domain vision statement in three sentences.
Then point at the files that implement that statement.
If they are mixed with generic code, sketch how you would separate them.

---

## 🔁 Module 4 · Before / After

**Before:** after Module 3 the code was safe to change, but spoke developer language: a status string `"accepted"` that reviewers misread, a separate check for confidence, and no place for a partner's data.

*File: [`projects/company-enricher/stages/03-change-safely/enricher/enricher.py`](../projects/company-enricher/stages/03-change-safely/enricher/enricher.py)*

```python
ACCEPTED = "accepted"
NEEDS_REVIEW = "needs_review"

WEAK_EVIDENCE = "weak_evidence"
NO_WEBSITE = "no_website"
```

**After:** the code speaks the reviewers' language.
Outcomes and reasons are enums, confidence and evidence are value objects that guard their own rules, companies have identity, the review rule is a named policy, a partner directory is translated at the border, and the core lives in its own folder with a test to keep it there.

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

---

## 📖 Curated Resources

1. **Domain reading:** Eric Evans, *Domain-Driven Design*, Chapter 15, "Distillation" (to verify against book).
   - 🔗 [DDD resources from Domain Language](https://www.domainlanguage.com/ddd/)
   - Why: core domain, generic subdomains, and the vision statement.
2. **[Python documentation: ast](https://docs.python.org/3/library/ast.html)**
   - Why: how `test_layers.py` reads imports without running the code.
3. **[Python tutorial: packages](https://docs.python.org/3/tutorial/modules.html#packages)**
   - Why: how the `core` and `adapters` folders become importable packages.
4. **Free sources:** Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf) (Chapter 21, "Decide What Matters") and Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) (the distillation patterns).
   - Why: both authors' own words on finding and protecting what matters.

---

## 🤔 Reflection Questions

1. **Comprehension:** What makes a part of a system "core" rather than "generic"?
2. **Application:** Is the keyword classifier core or generic? Would your answer change if you replaced it with a bought machine-learning model?
3. **Connection:** Which earlier day made the core/adapters split cheap to do now?
4. **Personal:** In your work, where does most design effort go: the core, or the generic parts?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 16: Turn qualities into measurable requirements](../week-03/day-16-measurable-requirements.md). Module 5 begins: the model fits the business, so now the data it keeps has to evolve without breaking.

**Before moving on, make sure you can:**

- [ ] Classify each part of the service as core, supporting, or generic.
- [ ] State the core's purpose in one paragraph.
- [ ] Explain how `test_layers.py` protects the core.

[← Previous: Day 14 Protect context boundaries](./day-14-context-boundaries.md) | [Course Home](../README.md) | [Next: Day 16 Turn qualities into measurable requirements →](../week-03/day-16-measurable-requirements.md)
