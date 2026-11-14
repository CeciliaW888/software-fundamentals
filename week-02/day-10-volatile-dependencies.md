# Day 10: Put volatile dependencies at boundaries

[← Previous: Day 9 Tests are executable evidence](./day-09-tests-are-evidence.md) | [Course Home](../README.md) | [Next: Day 11 Refactor under evidence →](./day-11-refactor-under-evidence.md)

> 📍 **Where we are in the story:** Week 2 · The structure is clearer. Now you learn to change it without breaking what already works.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Identify the volatile dependencies of the Company Enricher: the website, the network, and the clock.
2. Describe what the service needs from a website source as a small Protocol.
3. Put real HTTP behind one adapter with a timeout, and test it without a network.
4. Inject the clock so time-dependent behaviour can be tested.

**Plain idea:** the parts most likely to change or fail belong at the edge, behind a small door the rest of the code can't see past.

**Difficulty:** 🟡 Intermediate\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 3 · Change safely (lesson 0010)

---

## 📚 Core Concepts

### Observe: what is likely to change

Ask of every dependency: how likely is it to change, and how likely is it to fail?

| Dependency | Likely to change? | Likely to fail? |
|---|---|---|
| Keyword counting | rarely | no |
| Where About pages come from | yes: sample data today, real websites later | yes: timeouts, missing pages |
| The current time | it changes every second | no, but tests cannot predict it |
| The store | yes: memory today, a database in Module 5 | yes |

The volatile ones are the website source, the clock, and the store.
In stage 02, `CompanyWebsites` reads sample data directly, and nothing in the code shows how a real website would fit in.

### Say it plainly: a small door at the edge

Stage 03 draws a line.
The core of the service, `Enricher`, only ever asks one question of a website source: give me the About page for this company name, or tell me there isn't one.
That question is written down as `WebsiteSource`.
Any object with an `about_page` method that returns an `AboutPage` or raises `WebsiteUnavailable` can be used.

Two objects answer it today:

- `SampleWebsiteSource` reads the made-up sample companies. Tests and the tracer bullet use it.
- `HttpWebsiteSource` fetches a real page, strips the HTML to text, and turns network errors into `WebsiteUnavailable`. It is the only code that knows about URLs, HTML, and timeouts.

The clock gets the same treatment.
`Enricher` takes a `clock` argument, a function returning the current time, with the real clock as the default.
Tests pass a function that always returns the same moment.

The HTTP adapter has one more door inside it: the `fetch` function.
Its tests pass a fake `fetch` that returns a fixed HTML string or raises `TimeoutError`, so the adapter's own logic is tested without the network.

### Name it: boundaries, adapters, protocols, dependency injection

A **boundary** is where your code meets something it does not control.
An **adapter** is the code at that boundary that translates between the outside world's terms and yours.
In Python, a `typing.Protocol` describes the methods an object must have without requiring it to inherit from anything.
Passing a dependency in, instead of letting the code fetch it itself, is called **dependency injection**.

John Ousterhout's *A Philosophy of Software Design* gives the reasons in Chapter 5, "Information Hiding (and Leakage)": details such as HTML parsing and timeouts are hidden in one module.
Chapter 7, "Different Layer, Different Abstraction", explains why each layer should speak its own vocabulary: the core talks about About pages, the adapter about URLs and bytes.
Chapter 8, "Pull Complexity Downwards", is why the adapter, not every caller, deals with network errors.

Ousterhout's Chapter 6, "General-Purpose Modules are Deeper", checked in Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf), explains why `WebsiteSource` is shaped the way it is: the interface is general enough that sample data, real HTTP, and a test fake all fit behind it, while each implementation stays as simple as today's need.
*The Pragmatic Programmer*'s Topic 28, "Decoupling", gives the same direction as Tip 48 (p. 136 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)): if something outside the code is important enough to share, put an API in front of it.

> **Key Insight:** Hide each volatile thing behind the smallest interface the core needs, and the core never changes when it does.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Volatile dependency** | Something the code relies on that is likely to change or fail, such as a network service or the clock. | Course-authored plain definition |
| **Boundary** | The point where this code meets another system or responsibility. | Standard software vocabulary; this plain definition is course-authored |
| **Adapter** | Code at a boundary that translates between an outside system and the rest of the service. | Standard software vocabulary; this plain definition is course-authored |
| **Protocol** | A Python type that lists the methods an object must have, without requiring inheritance. | Official Python vocabulary ([typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)) |
| **Dependency injection** | Passing a dependency in from outside instead of creating or finding it inside. | Standard software vocabulary; this plain definition is course-authored |
| **Timeout** | A limit on how long to wait for an answer before giving up. | Official Python vocabulary ([urllib.request.urlopen](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen)) |

---

## 💻 Code Examples

### Example 1: What the core needs, written down

*File: [`projects/company-enricher/stages/03-change-safely/enricher/website.py`](../projects/company-enricher/stages/03-change-safely/enricher/website.py)*

```python
class WebsiteSource(Protocol):
    def about_page(self, company_name: str) -> AboutPage:
        """Return the company's About page or raise WebsiteUnavailable."""
```

**What's happening:** this is the whole door.
Anything with this method can be a website source, including a test's fake.

### Example 2: The only code that knows about HTTP

*File: [`projects/company-enricher/stages/03-change-safely/enricher/website.py`](../projects/company-enricher/stages/03-change-safely/enricher/website.py)*

```python
def about_page(self, company_name):
    url = self._about_urls.get(company_name)
    if url is None:
        raise WebsiteUnavailable(company_name)
    try:
        html = self._fetch(url, self._timeout_seconds)
    except OSError as error:
        raise WebsiteUnavailable(f"{company_name}: {error}") from error
    extractor = _TextExtractor()
    extractor.feed(html)
    text = " ".join(part for part in extractor.parts if part)
    if not text:
        raise WebsiteUnavailable(f"{company_name}: About page has no text")
    return AboutPage(url=url, text=text)
```

**What's happening:** network errors (Python's `TimeoutError` is a kind of `OSError`) become the core's own `WebsiteUnavailable`, and HTML becomes plain text.
The core never sees an `OSError` or a tag.

### Example 3: Testing the adapter with no network

*File: [`projects/company-enricher/stages/03-change-safely/tests/test_http_source.py`](../projects/company-enricher/stages/03-change-safely/tests/test_http_source.py)*

```python
def test_network_error_becomes_website_unavailable():
    def fetch(url, timeout_seconds):
        raise TimeoutError("timed out")

    with pytest.raises(WebsiteUnavailable):
        HttpWebsiteSource(URLS, fetch=fetch).about_page("Saltwater Kitchen")
```

**What's happening:** the fake `fetch` simulates a timeout instantly, so the test is fast and never touches the internet.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which dependency is NOT volatile for this service?**

- A. The source of About pages
- B. The keyword-counting rule
- C. The current time
- D. The store

<details>
<summary>Answer</summary>

**B.** Keyword counting is the service's own stable logic. Websites, time, and storage either change, fail, or are unpredictable.

</details>

**Q2. Why does `HttpWebsiteSource` turn `OSError` into `WebsiteUnavailable`?**

- A. Because `OSError` cannot be caught
- B. To hide every bug
- C. So the core only needs to know its own exception
- D. Because Python requires it

<details>
<summary>Answer</summary>

**C.** The adapter translates the outside world's errors into the core's vocabulary, so the core's `try`/`except` from Day 8 keeps working with any source.

</details>

**Q3. What does a Protocol let `Enricher` accept?**

- A. Only subclasses of `WebsiteSource`
- B. Only objects from the standard library
- C. Only real HTTP sources
- D. Any object with a matching `about_page` method

<details>
<summary>Answer</summary>

**D.** Protocols describe shape, not ancestry, so a test fake works without inheriting anything.

</details>

### Exercise 2 · Change: add a file-based source (⏱️ ~20 min)

**Goal:** Prove the boundary works by adding a third source without touching `Enricher`.

**Instructions:**
1. In `stages/03-change-safely/enricher/website.py`, add `JsonFileWebsiteSource(path)` that reads a JSON file shaped like `SAMPLE_WEB`.
2. It must return an `AboutPage` or raise `WebsiteUnavailable`, nothing else.
3. Write a test using pytest's `tmp_path` fixture to create the file.
4. Run the tracer bullet with your source and check no line of `enricher.py` changed: `git diff --stat`.

<details>
<summary>Hint</summary>

`json.loads(path.read_text())` gives you the dictionary; then reuse `SampleWebsiteSource(pages)`.

</details>

### Exercise 3 · Transfer: find the volatile edges (⏱️ ~10 min)

List the external services, files, clocks, and random numbers a project of yours uses.
For each, write whether the core calls it directly or through an adapter, and what a test would need to replace it.

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapters 5, 7 and 8.
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: information hiding, layers with their own vocabulary, and pulling complexity down.
2. **[Python documentation: typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)**
   - Why: how structural types like `WebsiteSource` work.
3. **[Python documentation: urllib.request.urlopen](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen)**
   - Why: the `timeout` argument used by the real fetch.
4. **[Python documentation: html.parser](https://docs.python.org/3/library/html.parser.html)**
   - Why: how the adapter turns HTML into text.
5. **Free source:** Ousterhout's free [2nd-edition extract](https://web.stanford.edu/~ouster/cgi-bin/aposd2ndEdExtract.pdf), Chapter 6.
   - Why: general-purpose interfaces in the author's words.

---

## 🤔 Reflection Questions

1. **Comprehension:** What does the core of the service know about websites now?
2. **Application:** Module 5 replaces the in-memory store with a database. Which parts of `Enricher` should change?
3. **Connection:** How does injecting the clock make a Day 9 promise testable?
4. **Critical Thinking:** Can a boundary be too narrow? What would you lose if `about_page` returned only the first sentence?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 11: Refactor under evidence](./day-11-refactor-under-evidence.md). You will improve the code's structure in small, tested steps.

**Before moving on, make sure you can:**

- [ ] Name the volatile dependencies of the service.
- [ ] Explain what an adapter translates.
- [ ] Test code that uses the network or the clock without either.

[← Previous: Day 9 Tests are executable evidence](./day-09-tests-are-evidence.md) | [Course Home](../README.md) | [Next: Day 11 Refactor under evidence →](./day-11-refactor-under-evidence.md)
