# Day 3: Follow the data and outside changes

[← Previous: Day 2 Know what a function promises](./day-02-what-a-function-promises.md) | [Course Home](../README.md) | [Next: Day 4 Recognise complexity by its symptoms →](./day-04-complexity-symptoms.md)

> 📍 **Where we are in the story:** Week 1 · You've just inherited the script. Before changing anything, you learn to read it.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Trace one company name from input to saved category suggestion.
2. List every input a function uses, including inputs that are not parameters.
3. Point out every change a function makes outside its return value.
4. Name the outside systems a function depends on.

**Plain idea:** before you change a function, know where its data comes from and where its effects go.

**Difficulty:** 🟢 Beginner\
**Estimated Time:** 25 minutes (10 reading + 15 hands-on)\
**Module:** 1 · Read code before changing it (lesson 0003)

---

## 📚 Core Concepts

### Observe: follow one company through the service

Pick one company and follow it: Saltwater Kitchen.
The main function in the Module 1 code is `suggest_company_category`.
It receives three things: the company name, a classifier, and a store.

Now read the body line by line and write down what each step touches.

1. `find_official_website("Saltwater Kitchen")` looks the name up in `SAMPLE_WEB` and returns `https://saltwaterkitchen.example`.
2. `read_about_page(...)` searches `SAMPLE_WEB` again and returns the About-page text.
3. `summarise_business_activity(...)` keeps the first sentence: "A seaside restaurant and cafe serving breakfast, lunch and dinner, with catering for events".
4. `classifier.suggest(...)` counts category keywords and returns Food & Hospitality with confidence 1.0.
5. The confidence is at least 0.82, so `store.save(...)` records the suggestion, and the function returns it.

Notice step 1.
`SAMPLE_WEB` is not a parameter.
The function reads it anyway, from a module-level variable.
If someone edits that dictionary, the function's answer changes, even though nobody passed it anything new.

### Say it plainly: four questions for every function

A function can be fully described by four lists:

| Question | Saltwater Kitchen trace |
|---|---|
| What comes in? | The company name, the classifier, the store, **and the `SAMPLE_WEB` data it reads on its own** |
| What goes out? | A suggestion with a category and a confidence, or `None` |
| What else changes? | The store gains one saved suggestion |
| What can fail? | `WebsiteUnavailable` when the company is not in the sample web |

The bold part is the one people miss.
Parameters are easy to see because they sit in the function's first line.
Data read from a global variable, a file, a database, a clock, or the network is just as much an input, but you only find it by reading the body.

The same is true for outside changes.
The return value is visible at every call.
A save, a sent email, or a written file is invisible at the call site unless the name or the docstring tells you.

### Name it: inputs, outputs, side effects, dependencies

Programmers have names for these four lists.

- **Inputs** and **outputs** are what goes in and what comes back.
- A **side effect** is a change outside the return value, such as saving data.
- An **external dependency** is something outside the function that it relies on, such as the website data.
- A **hidden dependency** is an external dependency that is not visible in the function's parameters.

John Ousterhout's *A Philosophy of Software Design* calls the problem behind hidden dependencies an **unknown unknown**: something you need to know to change the code safely, with nothing in the code telling you that you need to know it (Chapter 2, "The Nature of Complexity").
Chapter 5, "Information Hiding (and Leakage)", adds a second warning.
Look at `read_about_page`: it loops over every page to find a URL that `find_official_website` already had.
Two functions both know how `SAMPLE_WEB` is shaped.
If its shape changes, both must change.

*The Pragmatic Programmer*'s Topic 28, "Decoupling", warns about exactly the `SAMPLE_WEB` problem.
Two of its tips (both p. 136 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)) are "Avoid Global Data" and "If It's Important Enough To Be Global, Wrap It in an API": global data is a hidden input to every function that reads it.
Day 5 follows that advice and wraps the website data in one module.

> **Key Insight:** A function's real inputs and outputs are everything it reads and changes, not just its parameters and return value.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Input** | Any data a function uses to produce its result, whether passed in or read from elsewhere. | Course-authored plain definition |
| **Output** | The value a function gives back to its caller. | Course-authored plain definition |
| **Side effect** | A change outside the returned value, such as saving data, sending a message, or modifying an input. | Standard software vocabulary; [PEP 257](https://peps.python.org/pep-0257/#multi-line-docstrings) asks docstrings to describe side effects |
| **External dependency** | Something outside the function that it relies on, such as a website, file, database, or clock. | Standard software vocabulary; this plain definition is course-authored |
| **Hidden dependency** | An external dependency that does not appear in the function's parameters. | Course-authored teaching term |
| **Unknown unknown** | Something you must know to change code safely, with no sign in the code that you need to know it. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2 |
| **Information leakage** | The same design knowledge appearing in more than one module, so a change to it touches all of them. | Paraphrased from John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 5 |

---

## 💻 Code Examples

### Example 1: A hidden input

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
def find_official_website(company_name):
    """Return the company's website address, or raise WebsiteUnavailable."""
    page = SAMPLE_WEB.get(company_name)
    if page is None:
        raise WebsiteUnavailable(company_name)
    return page["url"]
```

**What's happening:** the only parameter is the name, but the answer also depends on `SAMPLE_WEB`, a module-level dictionary.
Tests that change `SAMPLE_WEB` change this function's behaviour without calling it differently.

### Example 2: Two functions that know the same thing

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
def read_about_page(website):
    """Return the About-page text published at a website address."""
    for page in SAMPLE_WEB.values():
        if page["url"] == website:
            return page["about"]
    raise WebsiteUnavailable(website)
```

**What's happening:** `read_about_page` searches the same data again, by URL.
Both functions know that a page is a dictionary with `"url"` and `"about"` keys.
That shared knowledge is leakage; Day 5 removes it.

> **💡 Try it:** run `python enricher.py` inside `stages/01-read-code` and check that every line of output matches the trace you would predict.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Which of these is an input to `find_official_website` even though it is not a parameter?**

- A. The `SAMPLE_WEB` dictionary
- B. The company name
- C. The classifier
- D. The return value

<details>
<summary>Answer</summary>

**A.** The function reads SAMPLE_WEB from the module, so it is a hidden input. The name is a parameter, the classifier is not used here, and the return value is an output.

</details>

**Q2. Which line in `suggest_company_category` makes a change outside the return value?**

- A. `about_text = read_about_page(website)`
- B. `store.save(company_name, suggestion)`
- C. `if suggestion.confidence < 0.82:`
- D. `return suggestion`

<details>
<summary>Answer</summary>

**B.** Saving to the store is a side effect: it changes state that other code can see later. The other lines read data, compare values, or return.

</details>

**Q3. Why is it a problem that both `find_official_website` and `read_about_page` know the shape of `SAMPLE_WEB`?**

- A. It makes the code run twice as slowly.
- B. Python forbids two functions reading one variable.
- C. A change to the data's shape must be made in two places.
- D. It hides the return value from the caller.

<details>
<summary>Answer</summary>

**C.** Shared design knowledge is information leakage: one change to the shape now touches two functions. Speed is not the issue here, and Python allows shared reads.

</details>

### Exercise 2 · Change: write a data trace (⏱️ ~12 min)

**Goal:** Trace a company that fails, not one that succeeds.

**Instructions:**
1. Open `stages/01-read-code/enricher.py`.
2. Follow `suggest_company_category("Ghost Gum Traders", ...)` line by line.
3. Fill in the four-question table for this call: what comes in, what goes out, what else changes, what can fail.
4. Run `python -m pytest -q` in the same folder and find the test that proves your answer.

<details>
<summary>Check your trace</summary>

Comes in: the name, the classifier, the store, and `SAMPLE_WEB`.
Goes out: nothing; the function raises `WebsiteUnavailable` at the first step.
Changes: nothing; the store is untouched.
The test is `test_unknown_company_raises_website_unavailable` in `tests/test_promises.py`.

</details>

### Exercise 3 · Transfer: find a hidden dependency (⏱️ ~10 min)

Pick a function you use at work or in a project.
List everything it reads that is not a parameter: globals, files, environment variables, the current time, network calls.
For each one, write how a test would control it.

---

## 🔁 Module 1 · Before / After

**Before:** the inherited script runs, but nobody can say what goes in, what comes back, what gets saved, or what can fail without reading every line.

*File: [`projects/company-enricher/stages/00-inherited/enricher.py`](../projects/company-enricher/stages/00-inherited/enricher.py)*

```python
def go(n, db):
    d = SAMPLE_WEB.get(n)
    if not d:
        raise Exception("no site")
    x = d["about"].split(".")[0]
    p = M().predict_proba([x])[0]
    i = p.index(max(p))
    if max(p) < 0.82:
        return None
    db.append((n, CATS[i], max(p)))
    return CATS[i]
```

**After:** the decisions are unchanged: every sample company gets the same category as before, and `tests/test_same_decisions.py` proves it.
What changed is that a reader knows the job, the inputs, the possible results, the outside change, and the failure before opening the body.

*File: [`projects/company-enricher/stages/01-read-code/enricher.py`](../projects/company-enricher/stages/01-read-code/enricher.py)*

```python
def suggest_company_category(
    company_name,
    classifier,
    store,
):
    """Suggest a business category for one company.

    Reads the company's official website
    and About page.
    Returns the saved suggestion when its
    confidence is at least 0.82.
    Returns None when evidence is weaker.
    Saves an accepted suggestion to store.
    Raises WebsiteUnavailable when no
    suitable page can be read.
    """
    ...
```

---

## 📖 Curated Resources

1. **Main design reading:** John Ousterhout, *A Philosophy of Software Design*, 2nd ed., Chapter 2, "The Nature of Complexity", and Chapter 5, "Information Hiding (and Leakage)".
   - 🔗 [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)
   - Why: names the cost of knowledge that the code does not show.
2. **[PEP 257: Multi-line Docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings)**
   - Why: lists side effects and exceptions as things a function's docstring should state.
3. **[Python tutorial: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)**
   - Why: explains how a function reads global names, which is how `SAMPLE_WEB` reaches `find_official_website`.
4. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 28, "Decoupling".
   - 🔗 [Official tip list](https://pragprog.com/tips/)
   - Why: Tips 47 and 48, on global data as a hidden coupling.

---

## 🤔 Reflection Questions

1. **Comprehension:** Which of the four questions does a function's first line answer, and which does it never answer?
2. **Application:** How would you change `find_official_website` so a test could give it different website data without editing a global?
3. **Connection:** How does the Day 2 docstring help a reader who has not done this trace?
4. **Critical Thinking:** Is reading the current time a hidden input? What would a test of time-dependent code need?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 4: Recognise complexity by its symptoms](./day-04-complexity-symptoms.md). You can read the script now; next you learn to spot what makes it hard to change.

**Before moving on, make sure you can:**

- [ ] List a function's inputs, including the ones that are not parameters.
- [ ] Point at every side effect in a function body.
- [ ] Explain why two functions sharing knowledge of a data shape is a risk.

[← Previous: Day 2 Know what a function promises](./day-02-what-a-function-promises.md) | [Course Home](../README.md) | [Next: Day 4 Recognise complexity by its symptoms →](./day-04-complexity-symptoms.md)
