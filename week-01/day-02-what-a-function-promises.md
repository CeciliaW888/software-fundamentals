# Day 2: Know what a function promises

[← Previous: Day 1 Use names that explain the job](./day-01-names-that-explain-the-job.md) | [Course Home](../README.md) | [Next: Day 3 Follow the data and outside changes →](./day-03-follow-the-data.md)

> 📍 **Where we are in the story:** Week 1 · You've just inherited the script. Before changing anything, you learn to read it.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Before reading every line of a function, find what goes in, what may come back, what else changes, and what can fail.
2. Describe one function clearly.
3. Test what other code is allowed to rely on.

**Plain idea:** other code should depend on a function's promised result, not on the temporary steps inside it.

**Difficulty:** 🟢 Beginner\
**Estimated Time:** 12 minutes\
**Module:** 1 · Read code before changing it (lesson 0002)

---

## 📚 Core Concepts

### Observe: start with a real question

Our service receives a company name, finds the official website, reads its About page, summarises the business activity, and suggests a business category from a short, plain list.

If another part of the service uses that suggestion, what does it need to know?

| | Question | Answer for this service |
|---|---|---|
| **01 · IN** | What goes in? | A company name, a category classifier, and a place to save results. |
| **02 · OUT** | What may come back? | A category suggestion, or `None` when the evidence is not strong enough. |
| **03 · ELSE** | What else happens? | An accepted suggestion is saved; website or classification work may fail. |

### Say it plainly: read the work once

The first code example shows the whole flow.

Some facts affect other code.
A weak suggestion returns `None`.
A returned suggestion has already been saved.

Other facts are only today's method: which service finds the website, which tool reads the page, which model suggests the category, how often the service tries again, and where it saves the result.

### Name it: write down the promise

Python lets us place an explanation directly under the function name.
This is called a **docstring**.

The docstring in the second code example states the result, the low-confidence case, the saved change, and one failure.
`WebsiteUnavailable` is a course-authored name for the error raised when no suitable page can be read.

It leaves out replaceable details: which service finds the website, which tool reads the page, which model suggests the category, how often it tries again, and where it saves the result.

*The Pragmatic Programmer*'s Topic 23, "Design by Contract" (to verify against book), frames the same idea as a contract: what a routine expects before it runs, what it guarantees when it finishes, and what stays true throughout.
Its Tip 37 (p. 107 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)) is "Design with Contracts".
This course uses the plainer word *promise* until the idea is familiar.

> **Key Insight:** Before reading how a function works, list what goes in, what can come back, what else changes, and what can fail.

### Quick reference: four questions

Understand the result before getting lost in the steps used to produce it.
Quick test: can you use the function correctly without reading every line inside it?

| Ask | Company Enricher example |
|---|---|
| What goes in? | A company name, a category classifier, and a place to save results. |
| What can come back? | A category suggestion, or `None` when evidence is weak. |
| What else changes? | An accepted suggestion is saved before it is returned. |
| What can fail? | The official website or About page may not be found or read. |

Do not promise temporary details:

- A particular search engine
- A particular HTML-reading library
- Private helper names and call order
- Retry count unless another part of the system must rely on it
- A database or AI vendor that can be replaced

Remember the four plain questions first: input, result, outside change, and failure.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Function** | A named block of code that performs a job. | Official Python vocabulary ([Python tutorial](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)) |
| **Docstring** | Text inside a function that explains how to use it. | Official Python vocabulary ([PEP 257](https://peps.python.org/pep-0257/#what-is-a-docstring)) |
| **None** | Python's built-in marker for "no value here." | Official Python vocabulary ([Python documentation](https://docs.python.org/3/library/constants.html#None)) |
| **Interface** | What other code must know to use a function or module. | Standard software vocabulary; central in Ousterhout Chapter 4 (to verify against book) |
| **Implementation** | The steps currently used to do the work. | Standard software vocabulary; central in Ousterhout Chapter 4 (to verify against book) |
| **Side effect** | An outside change, such as saving data or sending a message. | Standard software vocabulary; [PEP 257](https://peps.python.org/pep-0257/#multi-line-docstrings) says function documentation should describe side effects |
| **Module** | A unit of code with an interface and an implementation. It can be a function, class, subsystem, or service. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 4 (to verify against book) |
| **Abstraction** | A simplified view of something that leaves out unimportant details. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 4 (to verify against book) |

**Two words you do not need yet:**

- **Contract** appears in broader software-engineering writing as shorthand for promised behaviour. The reviewed Ousterhout chapters do not use it, and this course does not require it.
- **Callable** is official Python vocabulary for anything that can be used with function-call syntax ([Python glossary](https://docs.python.org/3/glossary.html#term-callable)). This lesson uses the narrower word **function**.

---

## 💻 Code Examples

### Example 1: How the work happens today

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
def suggest_company_category(
    company_name,
    classifier,
    store,
):
    website = find_official_website(
        company_name
    )
    about_text = read_about_page(website)
    activity_summary = (
        summarise_business_activity(
            about_text
        )
    )
    suggestion = classifier.suggest(
        activity_summary
    )

    if suggestion.confidence < 0.82:
        return None

    store.save(company_name, suggestion)
    return suggestion
```

**What's happening:** a weak suggestion returns `None`; a returned suggestion has already been saved.

### Example 2: Understand the function without opening its body

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
def suggest_company_category(
    company_name,
    classifier,
    store,
):
    """Suggest a business category.

    Find the official website.
    Read its About page.
    Use classifier to propose a category.
    Use store to save an accepted result.
    Return the saved result when its
    confidence is at least 0.82.
    Return None when evidence is weaker.

    Raise WebsiteUnavailable when no
    suitable page can be read.
    """
    ...
```

**What's happening:** the docstring states the result, the low-confidence case, the saved change, and one failure.

### Example 3: A test that can survive an internal rewrite

A useful test checks what other code can observe.
It does not check which helper or library was used.

*File: [`projects/company-enricher/stages/01-read-code/tests/test_promises.py`](../projects/company-enricher/stages/01-read-code/tests/test_promises.py)*

```python
def test_weak_suggestion_is_not_saved():
    classifier = classifier_returning(
        category="Manufacturing",
        confidence=0.61,
    )
    store = recording_store()

    result = suggest_company_category(
        "Lantern Lane Bakery",
        classifier,
        store,
    )

    assert result is None
    assert store.saved_suggestions == []
```

**What's happening:** the test checks two visible results: the function returns `None`, and the store remains unchanged.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check: which fact must code using this function be able to rely on? (⏱️ ~1 min)

<details>
<summary>Choose an answer, then open to check</summary>

- **A returned suggestion has already been saved.** *Correct. Saving the accepted suggestion changes the state that other code can observe.*
- Google is used to find the official website. *The search provider can change without changing the function's useful result.*
- A particular tool reads the About page. *The page-reading tool can change while the promised result stays the same.*
- The classifier tries exactly two times. *The number of attempts is an internal choice unless the function promises it.*

</details>

### Exercise 2 · Change: promise or temporary detail? (⏱️ ~3 min)

**Goal:** Select the three facts that other code needs to know.
Leave the two replaceable details unselected.

1. Returns a saved category suggestion when confidence meets the threshold.
2. Returns `None` when the website evidence is not strong enough.
3. Raises `WebsiteUnavailable` when no suitable page can be read.
4. Uses one named search engine to find every company website.
5. Uses one named tool to read every About page.

<details>
<summary>Check your choices</summary>

Facts 1, 2, and 3 are promises.
Facts 4 and 5 are temporary details: the search engine and the page-reading tool can change without changing the function's useful result.

</details>

### Exercise 3 · Transfer: try it elsewhere (⏱️ ~8 min)

Choose one function you did not write.
Before opening its body, write four lines: input, possible result, other change, and failure.
Then read the body to check whether your list is complete.

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, Chapter 4 on interface versus implementation and Chapter 13 (to verify against book) on useful function documentation.
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: the design advice behind this lesson.
2. **[PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings)**
   - Why: says a function docstring should cover behaviour, arguments, returns, outside changes, errors, and calling restrictions when applicable.
3. **[Python glossary: callable](https://docs.python.org/3/glossary.html#term-callable)**
   - Why: the broader Python term behind "function."
4. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 23, "Design by Contract" (to verify against book).
   - 🔗 [Official tip list](https://pragprog.com/tips/)
   - Why: Tip 37, on stating what code expects and guarantees.

---

## 🤔 Reflection Questions

1. **Comprehension:** Why does the test in Example 3 still pass if the service switches to a different search engine?
2. **Application:** Which of the four questions does a missing `Raises` line in a docstring leave unanswered?
3. **Connection:** How does a clear name from Day 1 make a function's promise easier to state?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 3: Follow the data and outside changes](./day-03-follow-the-data.md), tracing company name to category suggestion and evidence.

**Before moving on, make sure you can:**

- [ ] List a function's input, possible result, other change, and failure.
- [ ] Tell a promise from a temporary detail.
- [ ] Write a test that checks what other code can observe.

[← Previous: Day 1 Use names that explain the job](./day-01-names-that-explain-the-job.md) | [Course Home](../README.md) | [Next: Day 3 Follow the data and outside changes →](./day-03-follow-the-data.md)
