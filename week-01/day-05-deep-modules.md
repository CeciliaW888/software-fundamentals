# Day 5: Build deep modules

[← Previous: Day 4 Recognise complexity by its symptoms](./day-04-complexity-symptoms.md) | [Course Home](../README.md) | [Next: Day 6 Split by information, not length →](./day-06-split-by-information.md)

> 📍 **Where we are in the story:** Week 1 · You can read the script now. Before it grows, you learn to tame its complexity.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Compare a module's interface with the work it hides.
2. Recognise shallow modules and pass-through functions.
3. Replace a chain of small website helpers with one deep module.
4. Explain why the deep version is easier for every caller.

**Plain idea:** a good module does a lot of work behind a small, simple way of asking for it.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 35 minutes (15 reading + 20 hands-on)\
**Module:** 2 · Control complexity (lesson 0005)

---

## 📚 Core Concepts

### Observe: what a caller must know today

In the Module 1 code, getting a company's activity takes three calls in a fixed order:

1. `find_official_website(company_name)` returns a URL.
2. `read_about_page(website)` takes that URL and returns text.
3. `summarise_business_activity(about_text)` returns the first sentence.

Every caller must know all three names, their order, and that a URL passes from step 1 to step 2.
The URL is not useful to the caller; it only exists to be handed back.
And as Day 3 showed, two of the helpers both know how the website data is shaped.

### Say it plainly: cost versus benefit of a module

Think of any piece of code as a box.
The outside of the box is what callers must learn: names, parameters, rules, and failures.
The inside is the work the box does for them.

A box is worth having when the inside is large and the outside is small.
The three website helpers are the opposite: each one does very little, and together they ask the caller to learn a lot.

The Module 2 code has one box instead: `CompanyWebsites`.
A caller asks one question, "what does this company say about itself?", and gets an `AboutPage` back.
How the website is found, how the page is read, and where the data lives are all inside.
Even "the first sentence states the main activity" is now a property of the page, `main_activity`, instead of a separate step every caller must remember.

### Name it: deep modules, shallow modules, pass-through methods

John Ousterhout's *A Philosophy of Software Design* uses **module** for any unit with an interface and an implementation, from a function to a service (Chapter 4, "Modules Should Be Deep" (to verify against book)).
A **deep module** offers powerful functionality through a simple interface.
A **shallow module** has an interface that is complicated relative to what it does, so it adds more to learn than it saves.

Chapter 7, "Different Layer, Different Abstraction" (to verify against book), names a common shallow pattern: the **pass-through method**, which does little except hand its arguments to another method.
Chapter 8, "Pull Complexity Downwards" (to verify against book), gives the direction of the fix: it is better for the module to absorb complexity than for every caller to deal with it.

The `main_activity` property is a small example of pulling complexity down.
The rule "use the first sentence" now lives in one place, inside the module that owns the page.

Ousterhout's Chapter 6, "General-Purpose Modules are Deeper", checked in Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf), adds a second test of a good interface.
He recommends making modules *somewhat general-purpose*: the implementation does what today's callers need, but the interface is not tied to one particular use.
`CompanyWebsites.about_page` passes that test.
It answers a general question about any company, and says nothing about keywords or categories, so a classifier, a report, or a reviewer screen can all use it.

> **Key Insight:** Judge a module by how much it saves its callers, not by how short it is.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Module** | A unit of code with an interface and an implementation, from a function to a whole service. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 4 (to verify against book) |
| **Interface** | Everything someone working elsewhere must know to use the module. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 4 (to verify against book) |
| **Deep module** | A module that provides powerful functionality behind a simple interface. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 4 (to verify against book) |
| **Shallow module** | A module whose interface is complicated compared with the functionality it provides. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 4 (to verify against book) |
| **Pass-through method** | A method that does little except pass its arguments to another method. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 7 (to verify against book) |
| **Property** | A Python attribute whose value is computed by a method each time it is read. | Official Python vocabulary ([built-in functions: property](https://docs.python.org/3/library/functions.html#property)) |
| **Somewhat general-purpose** | A module whose functionality meets today's needs while its interface is general enough for several uses. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 6, checked in the author's free extract |

---

## 💻 Code Examples

### Example 1: Before, three helpers in a fixed order

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
def summarise_business_activity(about_text):
    """Return the first sentence, which usually states the main activity."""
    return about_text.split(".")[0]
```

**What's happening:** together with `find_official_website` and `read_about_page` from Day 3, this is the third step a caller must remember.
Each helper is short; the interface of the trio is long.

### Example 2: After, one deep module

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/website.py`](../projects/company-enricher/stages/02-control-complexity/enricher/website.py)*

```python
@dataclass(frozen=True)
class AboutPage:
    url: str
    text: str

    @property
    def main_activity(self):
        """The first sentence, which usually states what the business does."""
        return self.text.split(".")[0]


class CompanyWebsites:
    """One call answers "what does this company say about itself?"."""

    def __init__(self, pages=SAMPLE_WEB):
        self._pages = pages

    def about_page(self, company_name):
        page = self._pages.get(company_name)
        if page is None:
            raise WebsiteUnavailable(company_name)
        return AboutPage(url=page["url"], text=page["about"])
```

**What's happening:** callers learn one method and one result type.
The page data is passed in once, which also removes Day 3's hidden global: a test can hand `CompanyWebsites` any pages it likes.
The URL is still kept, inside `AboutPage`, because it is useful later as evidence.

### Example 3: The caller now

*File: [`projects/company-enricher/stages/02-control-complexity/enricher/enricher.py`](../projects/company-enricher/stages/02-control-complexity/enricher/enricher.py)*

```python
page = self._websites.about_page(company_name)
suggestion = self._classifier.suggest(page.main_activity)
```

**What's happening:** two lines replace the three-step chain, and neither line mentions URLs or data shapes.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. What makes the trio of website helpers shallow?**

- A. Each function is fewer than ten lines.
- B. They use a dictionary.
- C. Together they make callers learn three names, an order, and a URL hand-off for little work.
- D. They have docstrings.

<details>
<summary>Answer</summary>

**C.** Shallowness is about the ratio of interface to functionality. Short functions are not the problem; the amount callers must learn is.

</details>

**Q2. Where should the rule "the first sentence states the main activity" live?**

- A. In every caller that needs the activity
- B. In a comment at the top of the project
- C. In the classifier's keyword list
- D. In the module that owns the About page, as `main_activity`

<details>
<summary>Answer</summary>

**D.** Pulling the rule down into the page module means callers cannot forget or disagree about it.

</details>

**Q3. Which change would make `CompanyWebsites` shallower?**

- A. Making callers pass the page dictionary to every `about_page` call
- B. Adding caching inside `about_page`
- C. Raising `WebsiteUnavailable` for unknown companies
- D. Returning an `AboutPage` instead of a dictionary

<details>
<summary>Answer</summary>

**A.** Pushing the data back out to every call grows the interface without adding functionality. Caching inside the module would make it deeper, not shallower.

</details>

### Exercise 2 · Change: count what callers must learn (⏱️ ~15 min)

**Goal:** Measure depth.

**Instructions:**
1. List every name, parameter, ordering rule, and exception a caller must know to get a company's main activity in `stages/01-read-code`.
2. Do the same for `stages/02-control-complexity`.
3. Run both stages' tests to confirm both versions still make the same decisions: `python -m pytest -q` in each folder.

<details>
<summary>Check your count</summary>

Module 1: three function names, their order, the URL hand-off, the hidden `SAMPLE_WEB`, and `WebsiteUnavailable`.
Module 2: `CompanyWebsites`, `about_page`, `AboutPage.main_activity`, and `WebsiteUnavailable`.

</details>

### Exercise 3 · Transfer: find a pass-through (⏱️ ~10 min)

In code you know, find a function whose body is mostly one call to another function with the same arguments.
Decide whether it earns its place: does it hide a decision, or only add a name to learn?

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapters 4 to 8, especially Chapter 4, "Modules Should Be Deep" (to verify against book).
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: the source of deep and shallow modules.
2. **[Python documentation: dataclasses](https://docs.python.org/3/library/dataclasses.html)**
   - Why: how `AboutPage` gets its constructor and equality, and what `frozen=True` means.
3. **[Python documentation: property](https://docs.python.org/3/library/functions.html#property)**
   - Why: how `main_activity` is computed when read.
4. **Free source:** Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf), Chapter 6, "General-Purpose Modules are Deeper".
   - Why: the author's own explanation of general-purpose interfaces, free to read.

---

## 🤔 Reflection Questions

1. **Comprehension:** In your own words, what is the difference between a short module and a deep one?
2. **Application:** Day 10 will add a real HTTP website source. Which callers will need to change?
3. **Connection:** Which Day 4 symptom did the deep module reduce the most?
4. **Critical Thinking:** When could a deep module become too big to understand?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 6: Split by information, not length](./day-06-split-by-information.md). You will decide where to draw lines inside the classifier.

**Before moving on, make sure you can:**

- [ ] Compare a module's interface with its functionality.
- [ ] Spot a pass-through function.
- [ ] Explain what `CompanyWebsites` hides from its callers.

[← Previous: Day 4 Recognise complexity by its symptoms](./day-04-complexity-symptoms.md) | [Course Home](../README.md) | [Next: Day 6 Split by information, not length →](./day-06-split-by-information.md)
