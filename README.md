# Software Fundamentals

> **From AI-written script to software you trust.**

An AI assistant wrote a working script that finds a company's website and suggests its business category.
Over six modules you **inherit it**, **tame its complexity**, **change it safely**, **model the business**, **design data that evolves**, and **operate it**, until it is software you would trust in production.

[![PWA Ready](https://img.shields.io/badge/PWA-Ready-c4825a)](https://ceciliaw888.github.io/software-fundamentals/)
[![Days](https://img.shields.io/badge/Course-24_Days-blue.svg)](#course-outline)

**▶ Read the course online: [ceciliaw888.github.io/software-fundamentals](https://ceciliaw888.github.io/software-fundamentals/)**
Or read the daily guides as Markdown, starting with [Day 1](week-01/day-01-names-that-explain-the-job.md).

## About This Course

The course assumes **no software-engineering background**.
Plain words and observable behaviour come first.
Technical terms appear only after the idea is concrete, and each term is labelled by its source.

A beginner-first, practice-led course for learning how to understand, design, test, and change reliable software.

Every lesson improves the same small Python service, the **Company Enricher**: it receives a company name, finds the official website, reads the About page, summarises the business's main activity, and suggests a category from a short, plain list, with its evidence, confidence, and review status.
See the [practice project](projects/company-enricher/README.md).

**Duration:** 24 days (4 weeks), one lesson per day
**Daily commitment:** about 30-45 minutes per lesson
**Language:** English
**Level:** Beginner, no software-engineering background
**Status:** all 24 days are written, and every code example comes from the runnable practice project.

## Learning Goals

By the end of this course, you will be able to:

- Read unfamiliar Python code and explain what goes in, what comes out, what else changes, and what can fail.
- Compare designs by how much they make a learner or maintainer hold in their head.
- Improve generated or inherited code without changing its intended behaviour.
- Model business rules without turning every noun into a class.
- Choose data and system designs from measurable needs.
- Run and change a service with tests, monitoring, safe deployment, and rollback.

## Course Outline

Each week holds whole modules.
Weeks 1 and 2 are the required core (modules 1-3) plus domain modeling; weeks 3 and 4 are data design and operations.
Each lesson follows the same loop: observe, say it plainly, name it, change, check, transfer.

### 🧭 Week 1: Read code and control complexity

| Day | Lesson | Module | Durable decision | Main sources | Status |
|---|---|---|---|---|---|
| 1 | [Use names that explain the job](week-01/day-01-names-that-explain-the-job.md) | 1 Read code | Make the business object, stage, unit, and decision visible | *APOSD* Ch. 14; *TPP* "Naming Things"; PEP 8 | ✅ Written |
| 2 | [Know what a function promises](week-01/day-02-what-a-function-promises.md) | 1 Read code | Separate what other code may rely on from how the work happens | *APOSD* Chs. 4, 13; PEP 257; *TPP* "Design by Contract" | ✅ Written |
| 3 | [Follow the data and outside changes](week-01/day-03-follow-the-data.md) | 1 Read code | Identify inputs, outputs, stored changes, and external dependencies | *APOSD* Chs. 2, 5 | ✅ Written |
| 4 | [Recognise complexity by its symptoms](week-01/day-04-complexity-symptoms.md) | 2 Complexity | Find change amplification, cognitive load, and unknown unknowns | *APOSD* Ch. 2; *TPP* "Software Entropy" | ✅ Written |
| 5 | [Build deep modules](week-01/day-05-deep-modules.md) | 2 Complexity | Hide useful complexity behind a small, complete interface | *APOSD* Chs. 4-8 | ✅ Written |
| 6 | [Split by information, not length](week-01/day-06-split-by-information.md) | 2 Complexity | Keep related knowledge together and independent knowledge apart | *APOSD* Ch. 9; *TPP* "DRY", "Orthogonality" | ✅ Written |
| 7 | [Design it twice](week-01/day-07-design-it-twice.md) | 2 Complexity | Compare alternatives before committing to structure | *APOSD* Ch. 11; *TPP* "Tracer Bullets", "Prototypes and Post-it Notes" | ✅ Written |

### 🛡️ Week 2: Change safely and model the domain

| Day | Lesson | Module | Durable decision | Main sources | Status |
|---|---|---|---|---|---|
| 8 | [Decide what each failure means](week-02/day-08-what-each-failure-means.md) | 3 Change safely | Prevent, hide, combine, or report errors intentionally | *APOSD* Ch. 10; Python docs; *TPP* "Dead Programs Tell No Lies", "Assertive Programming" | ✅ Written |
| 9 | [Tests are executable evidence](week-02/day-09-tests-are-evidence.md) | 3 Change safely | Test promised behaviour instead of internal trivia | pytest and Python docs; *TPP* "Test to Code", "Property-Based Testing" | ✅ Written |
| 10 | [Put volatile dependencies at boundaries](week-02/day-10-volatile-dependencies.md) | 3 Change safely | Isolate databases, models, clocks, and network clients | *APOSD* Chs. 5, 7-8 | ✅ Written |
| 11 | [Refactor under evidence](week-02/day-11-refactor-under-evidence.md) | 3 Change safely | Improve structure without changing behaviour | *APOSD* Ch. 16; *TPP* "Refactoring", "Version Control"; Git docs | ✅ Written |
| 12 | [Build language from examples](week-02/day-12-language-from-examples.md) | 4 Domain | Discover rules before naming abstractions | *DDD* Chs. 1-3 | ✅ Written |
| 13 | [Choose entities, values, and services deliberately](week-02/day-13-entities-values-services.md) | 4 Domain | Model identity, value, and operations only where behaviour requires them | *DDD* Chs. 4-6 | ✅ Written |
| 14 | [Protect context boundaries](week-02/day-14-context-boundaries.md) | 4 Domain | Stop external models leaking into the core | *DDD* Ch. 14 | ✅ Written |
| 15 | [Distil the core](week-02/day-15-distil-the-core.md) | 4 Domain | Spend design effort where differentiation lives | *DDD* Ch. 15 | ✅ Written |

### 🗄️ Week 3: Design data that can evolve

| Day | Lesson | Module | Durable decision | Main sources | Status |
|---|---|---|---|---|---|
| 16 | [Turn qualities into measurable requirements](week-03/day-16-measurable-requirements.md) | 5 Data | Define latency, reliability, load, and maintainability targets | *TPP* Topic 5 and Tip 8; measurement: official docs | ✅ Written |
| 17 | [Choose a data model from access patterns](week-03/day-17-data-model-from-access.md) | 5 Data | Match relationships and queries to the model | *DDD* Ch. 6 (repositories, relational mapping); data models: SQLite, PostgreSQL and Python docs | ✅ Written |
| 18 | [Understand storage trade-offs](week-03/day-18-storage-trade-offs.md) | 5 Data | Connect indexes and layout to read/write behaviour | *TPP* Topic 39, Tips 63 and 64; indexes: SQLite and PostgreSQL docs | ✅ Written |
| 19 | [Evolve schemas without coordinated deployment](week-03/day-19-evolve-schemas.md) | 5 Data | Preserve compatibility across versions | SQLite, PostgreSQL and Python docs; *TPP* Tip 18 and Topic 27 for small, reversible steps; *DDD* Ch. 6 on why schema changes are costly | ✅ Written |
| 20 | [Protect invariants under concurrency](week-03/day-20-invariants-under-concurrency.md) | 5 Data | Choose an isolation guarantee from the failure you must prevent | *TPP* Topic 34; *DDD* Ch. 6 (aggregates); isolation levels: database docs | ✅ Written |

### 🚀 Week 4: Operate what you build

| Day | Lesson | Module | Durable decision | Main sources | Status |
|---|---|---|---|---|---|
| 21 | [Observe promises and failures](week-04/day-21-observe-promises.md) | 6 Operate | Instrument what users depend on | *TPP* Topic 20 (tracing); OpenTelemetry, Python and OWASP docs | ✅ Written |
| 22 | [Deploy reversibly](week-04/day-22-deploy-reversibly.md) | 6 Operate | Make configuration, migration, rollout, and rollback explicit | *TPP* "Reversibility", "Configuration"; GitHub Actions and Git docs | ✅ Written |
| 23 | [Measure before optimizing](week-04/day-23-measure-before-optimizing.md) | 6 Operate | Locate the critical path before changing code | *APOSD* Ch. 20 | ✅ Written |
| 24 | [Design for expected failure](week-04/day-24-design-for-failure.md) | 6 Operate | Choose retries, timeouts, idempotency, and fallbacks from failure semantics | *APOSD* Ch. 10 (masking errors, retrying in one layer); Python, SQLite and HTTP (RFC 9110) docs | ✅ Written |

The full curriculum, with each lesson's practice change, exit evidence per module, and the proposed toolkit strand, is in [COURSE_DESIGN.md](COURSE_DESIGN.md).

## 🚀 Get Started

### Learn Online

Visit the course website on GitHub Pages (installable, works offline):

```
https://ceciliaw888.github.io/software-fundamentals/
```

### Learn Locally

```bash
git clone https://github.com/CeciliaW888/software-fundamentals.git
cd software-fundamentals
open week-01/day-01-names-that-explain-the-job.md
```

Run the practice project (Python 3.10 or later, with pytest):

```bash
pip install pytest
projects/company-enricher/run_all_tests.sh
```

To preview the website, serve the `website/` folder (module pages are fetched, so opening `index.html` directly from disk will not load them):

```bash
python3 -m http.server 8000 --directory website
```

### Install as PWA

1. Open the course website in Chrome or Edge.
2. Click the "Install" icon in the address bar, or the install button on the page.
3. Once installed, open it from your desktop or home screen; it works offline.

## 📦 Repo Structure

```
software-fundamentals/
├── README.md
├── COURSE_DESIGN.md                 # teaching model, source hierarchy, full curriculum
├── week-01/ … week-04/              # one Markdown guide per day: the single source for each lesson
├── projects/
│   └── company-enricher/            # the practice service, one runnable snapshot per module
│       ├── stages/00-inherited/     # the AI-written script you inherit
│       ├── stages/01-read-code/ … stages/06-operate/
│       └── run_all_tests.sh
├── diagrams/                        # Excalidraw sources
├── scripts/
│   ├── build_site.py                # Markdown guides → website modules, quizzes, flashcards
│   └── check_course.py              # snippets match the project, code parses, links work
├── .github/workflows/
│   ├── deploy.yml                   # publishes website/ to GitHub Pages
│   └── company-enricher-tests.yml   # runs every stage's tests on each push
└── website/                         # the PWA (styles.css and main.js from the learning-to-course skill, unmodified)
    ├── index.html  manifest.json  sw.js  offline.html
    ├── modules/  data/  diagrams/  icons/
    └── lessons/  reference/         # redirects from the old lesson URLs
```

## 🛠️ Working on the course

Edit the Markdown guide in `week-NN/`, then rebuild the website data and run the checks:

```bash
python3 scripts/build_site.py
python3 scripts/check_course.py --links
projects/company-enricher/run_all_tests.sh
```

Every Python and SQL example in a guide sits under a `*File: [...]*` line naming the project file it comes from, and `check_course.py` fails if the example no longer matches that file.
Days 1 and 2 keep hand-made website modules for their custom exercises; every other module is generated.

## Resources

No single book is treated as law.
Official Python and tool documentation define behaviour.

The course uses three main books:

- *A Philosophy of Software Design*, 2nd ed., by John Ousterhout ([book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)) is the main design spine.
- *The Pragmatic Programmer*, 20th Anniversary Edition (2019), by David Thomas and Andrew Hunt ([publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)) supports everyday habits and tools: duplication, contracts, failing early, testing, debugging, version control, and the shell.
- *Domain-Driven Design* by Eric Evans ([DDD resources](https://www.domainlanguage.com/ddd/)) supports selected business-language and modeling lessons.

Where none of the three books fits a lesson, the lesson says so plainly and relies on official documentation.
Every book citation, chapter or topic number, and paraphrase was checked against the full books; [docs/book-verification.md](docs/book-verification.md) records what was checked and what changed.

Behavioural and domain authority:

- [Python documentation](https://docs.python.org/3/) and [Python glossary](https://docs.python.org/3/glossary.html)
- [PEP 8](https://peps.python.org/pep-0008/) for naming and readability, [PEP 257](https://peps.python.org/pep-0257/) for docstrings
- [pytest documentation](https://docs.pytest.org/)
- [FastAPI](https://fastapi.tiangolo.com/) and [OpenTelemetry](https://opentelemetry.io/docs/) documentation when later modules need them

Each book's role, citation rules, and the known source gaps are in [COURSE_DESIGN.md](COURSE_DESIGN.md#sources).
