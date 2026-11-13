# Course design

This is the author's design document.
Learners start at the [README](README.md) or the [course website](https://ceciliaw888.github.io/software-fundamentals/).

## Mission

### Who this is for

This course is for a learner who can use technology but has no formal software-engineering background.
It must teach judgment without assuming prior knowledge of software vocabulary.

### Why

Build the judgment needed to understand, design, test, and change reliable software rather than merely assembling working demos.
Use one evolving Python service, the Company Enricher, so every idea becomes part of a recognisable system.
The story: an AI assistant wrote a working script, and over six modules the learner inherits it, tames its complexity, changes it safely, models the business, designs data that evolves, and operates it, until it is software they would trust in production.

### What “fundamental” means

A fundamental is a decision skill that survives changes in language, framework, vendor, and scale.
It should help a learner answer at least one of these questions:

- What does this code do?
- What can I change safely?
- Where should this job live?
- What evidence shows the system works?
- Which choice fits the real requirement?

### Success looks like

- Read unfamiliar Python code and explain what goes in, what comes out, what else changes, and what can fail.
- Compare designs by how much they make a learner or maintainer hold in their head.
- Improve generated or inherited code without changing its intended behaviour.
- Model business rules without turning every noun into a class.
- Choose data and system designs from measurable needs.
- Run and change a service with tests, monitoring, safe deployment, and rollback.

### Teaching rules

- Start with an observable example, not a definition.
- Use plain words before technical words.
- Define each new term at first use.
- Label terminology as official Python language, standard software vocabulary, a book’s term, domain language, or course shorthand.
- Put a sourced plain-language tooltip on the first useful occurrence of an unfamiliar term.
- Do not attribute a tooltip definition to a book unless the inspected text supports it.
- Never call general software vocabulary “ubiquitous language.”
- In DDD, ubiquitous language is the shared language of one business domain and team.
- Introduce one durable idea per lesson.
- Keep code examples short enough to understand in one sitting.
- Give immediate feedback and one transfer task.
- Add scale, distribution, or patterns only when the current service needs them.

### Out of scope

- Memorising framework APIs that can be looked up.
- Treating any author’s advice as a universal law.
- Jargon used only to sound technical.
- Building a course platform before the lessons prove useful.
- Chasing every new tool, framework, or headline.

## Learner and teaching model

The course assumes no software-engineering background.
A learner should not need to understand a technical term in order to reach the example that explains it.

Each lesson uses the same loop:

1. **Observe:** see a small piece of code or behaviour.
2. **Say it plainly:** describe what happened in everyday language.
3. **Name it:** introduce one technical term only after the idea is concrete.
4. **Change:** make one constrained improvement.
5. **Check:** receive immediate, concrete feedback.
6. **Transfer:** apply the decision to another example or review.

Every new term is labelled as official Python vocabulary, standard software vocabulary, a named book’s term, domain language, or course-authored shorthand.
General software vocabulary is not described as DDD ubiquitous language.
Ubiquitous language belongs to a specific business domain and team.
The first useful occurrence of unfamiliar terminology gets a keyboard-accessible and touch-accessible tooltip.
Each tooltip shows a plain definition followed by "Source: ..." in its text, and each day's Key Terminology table has a Source column.
Use a book definition only when the book actually defines the term; otherwise use official documentation, a domain authority, or label the definition as course-authored.

## One evolving practice service

The course follows one small Python service, the Company Enricher, from an AI-written script to an operable system.
Its description, category list, and ground rules are in [projects/company-enricher](projects/company-enricher/README.md).

Every lesson opens with a "Where we are in the story" line.
The last day of each module ends with a Before / After box showing the service before and after that module.

## Sources

### Source hierarchy

#### 1. Behavioural authority

Official language, standard-library, protocol, database, and tool documentation define actual behaviour.
Use these sources for syntax, semantics, compatibility, configuration, and operational guarantees.

#### 2. Core design spine

John Ousterhout’s *A Philosophy of Software Design, 2nd Edition* supplies the recurring vocabulary for complexity, decomposition, deep modules, information hiding, errors, documentation, consistency, alternatives, and performance.
Its principles are hypotheses to test against code, not rules to obey mechanically.

#### 3. Practice and workflow

David Thomas and Andrew Hunt’s *The Pragmatic Programmer, 20th Anniversary Edition* (2019), abbreviated *TPP*, supports lessons on everyday habits and tools: duplication of knowledge, orthogonality, software entropy, tracer bullets and prototypes, design by contract, failing early, refactoring, testing, debugging, version control, the shell, plain text, and estimating.
Ousterhout stays the design vocabulary; *TPP* adds working habits and fills the tooling gaps the design books leave open.
Cite *TPP* Topics by title, and check each against the 2019 edition before a lesson depends on it.

#### 4. Domain specialization

Eric Evans’s *Domain-Driven Design* supports selected lessons on knowledge discovery, ubiquitous language, model/code alignment, entities, value objects, services, aggregates, bounded contexts, anticorruption layers, and core-domain distillation.
Do not turn its tactical patterns into a default architecture.

These three books are the only main book sources.
Where none of them fits a lesson, the lesson says so plainly and relies on official documentation.
Citations not yet checked against the full books are marked "(to verify against book)" and listed in [docs/book-verification-todo.md](docs/book-verification-todo.md).

### Source roles and labels

#### Source policy

Sources have different jobs.
Official documentation defines behaviour.
Books provide design lenses.
Domain authorities define business classifications.
No source is treated as a universal rulebook.

The course has three main books: *A Philosophy of Software Design* (the design spine), *The Pragmatic Programmer*, and *Domain-Driven Design*.
Where none of them fits a lesson, the lesson says so rather than forcing a citation.

Each lesson labels unfamiliar words as one of:

- official Python vocabulary
- standard software-engineering vocabulary
- a named author’s term
- domain language for this service
- course-authored shorthand

#### Behavioural and domain authority

- [Python documentation](https://docs.python.org/3/) for language and standard-library behaviour
- [Python glossary](https://docs.python.org/3/glossary.html) for Python-specific vocabulary
- [PEP 8](https://peps.python.org/pep-0008/) for Python naming and readability conventions
- [PEP 257](https://peps.python.org/pep-0257/) for Python docstring conventions
- [pytest documentation](https://docs.pytest.org/) for tests and failure feedback
- [FastAPI documentation](https://fastapi.tiangolo.com/) when an HTTP boundary is introduced
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) when monitoring is introduced
- Database and deployment-platform documentation for product-specific guarantees

Public website text may be incomplete or ambiguous, so a website-based result in this course is called a **suggestion**, not an authoritative classification.
The service retains evidence, confidence, and review status.

#### Core design spine

##### *A Philosophy of Software Design, 2nd Edition* by John Ousterhout

**Role:** primary source for software design and refactoring judgment.

Use for complexity, modules, information hiding, errors, design alternatives, comments, naming, consistency, modifying code, and performance.
The author’s principles are tested against code rather than followed mechanically.

- [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)

#### Practice and workflow

##### *The Pragmatic Programmer: Your Journey to Mastery, 20th Anniversary Edition* by David Thomas and Andrew Hunt (2019)

**Role:** supporting source for everyday engineering habits and tools, not the course spine.

**Contribution:** practical habits that keep code changeable day to day, plus the shell, plain-text, version-control, and debugging skills the design books leave out.

Use for duplication of knowledge (DRY), orthogonality, software entropy (“broken windows”), tracer bullets and prototypes, design by contract, crashing early and assertions, refactoring, testing, debugging, version control, the shell and plain text, and estimating.
Where its advice overlaps with Ousterhout, *A Philosophy of Software Design* sets the vocabulary and this book adds practice examples.
The book is organised into numbered Topics; lessons cite a Topic by its title in this edition.
Check the cited Topic in the 2019 edition before using it as a tooltip or lesson source.

- [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)

#### Domain specialization

##### *Domain-Driven Design: Tackling Complexity in the Heart of Software* by Eric Evans

**Role:** source for selected domain-modeling lessons.

Use for learning the business problem, domain-specific shared language, model and code alignment, entities, value objects, services, context boundaries, and core-domain focus.
Do not treat its Java examples or tactical patterns as a default architecture.

In this course, terms such as **company**, **official website**, **About page**, **category evidence**, **category suggestion**, and **review required** may become domain language when their meanings are agreed.
Technical terms such as **function**, **exception**, and **return value** are not domain language.

- [Official DDD resources](https://www.domainlanguage.com/ddd/)

#### Known source gaps

Book citations that still need checking against the full books are listed in [docs/book-verification-todo.md](docs/book-verification-todo.md).
The topics below have no coverage in the three books' freely available material, and need a stable primary source:

- measurable quality requirements, data models, storage and indexing, schema evolution, and transaction isolation (Module 5; official database documentation covers behaviour, but no main book covers the design trade-offs)
- retries, timeouts, idempotency, and degraded modes (lesson 0024)
- secure software design and threat modeling (*The Pragmatic Programmer*’s “Stay Safe Out There” is an introduction only, not a threat-modeling source; to verify against book)
- deployment, migration, and rollback
- production incident response
- accessibility for developer-facing and user-facing interfaces

## Week and day pacing

The course uses the learning-to-course format: one Markdown guide per day in `week-NN/`, and one website module per day.
Each of the 24 lessons is one day, and lesson numbers map directly to days (lesson 0001 is Day 1, lesson 0024 is Day 24).
No review days are added, so no lesson is renumbered.

Weeks hold whole modules, so a module never splits across a week:

| Week | Days | Modules |
|---|---|---|
| 1 · Read code and control complexity | 1-7 | 1 Read code before changing it (0001-0003), 2 Control complexity (0004-0007) |
| 2 · Change safely and model the domain | 8-15 | 3 Change safely (0008-0011), 4 Model the domain (0012-0015) |
| 3 · Design data that can evolve | 16-20 | 5 Design data that can evolve (0016-0020) |
| 4 · Operate what you build | 21-24 | 6 Operate what you build (0021-0024) |

The weeks are 7, 8, 5, and 4 days long.
Keeping modules whole matters more than equal weeks.

Inside each daily guide, the lesson loop maps onto the skill's eight sections:

| Lesson loop | Daily-guide section |
|---|---|
| Observe | Core Concepts, "Observe" subsection, and Code Examples |
| Say it plainly | Core Concepts, "Say it plainly" subsection |
| Name it | Core Concepts, "Name it" subsection, and Key Terminology with a Source column |
| Change | Hands-On Exercises, "Change" exercise |
| Check | Hands-On Exercises, "Check" exercise, plus the day's quiz |
| Transfer | Hands-On Exercises, "Transfer" exercise, and Reflection Questions |

All 24 days are written.
Each lesson's code comes from `projects/company-enricher/stages/`, one runnable snapshot per module, and `scripts/check_course.py` checks that every example matches its file.

## Curriculum

### Module 1: Read code before changing it (required)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0001 Use names that explain the job | Make the business object, stage, unit, and decision visible | Rename an opaque category-suggestion function without changing behaviour | *APOSD* Ch. 14; *TPP* “Naming Things”; PEP 8 |
| 0002 Know what a function promises | Separate what other code may rely on from how the work happens | Describe and test one function’s promised behaviour | *APOSD* Chs. 4, 13; PEP 257; *TPP* “Design by Contract” |
| 0003 Follow the data and outside changes | Identify inputs, outputs, stored changes, and external dependencies | Trace company name to category suggestion and evidence | *APOSD* Chs. 2, 5 |

**Exit evidence:** the learner can explain an unfamiliar function’s job, inputs, possible results, outside changes, and failures before editing it.

### Module 2: Control complexity (required)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0004 Recognise complexity by its symptoms | Find change amplification, cognitive load, and unknown unknowns | Score one change before and after refactoring | *APOSD* Ch. 2; *TPP* “Software Entropy” |
| 0005 Build deep modules | Hide useful complexity behind a small, complete interface | Replace pass-through helpers with one coherent module | *APOSD* Chs. 4–8 |
| 0006 Split by information, not length | Keep related knowledge together and independent knowledge apart | Compare a short-function design with a deep-function design | *APOSD* Ch. 9; *TPP* “DRY - The Evils of Duplication”, “Orthogonality” |
| 0007 Design it twice | Compare alternatives before committing to structure | Produce two APIs and choose with explicit criteria | *APOSD* Ch. 11; *TPP* “Tracer Bullets”, “Prototypes and Post-it Notes” |

**Exit evidence:** the learner can defend a module boundary using total system complexity rather than file size or style rules.

### Module 3: Change safely (required)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0008 Decide what each failure means | Prevent, hide, combine, or report errors intentionally | Redesign one website or classification failure path | *APOSD* Ch. 10; Python docs; *TPP* “Dead Programs Tell No Lies”, “Assertive Programming” |
| 0009 Tests are executable evidence | Test promised behaviour instead of internal trivia | Add focused unit and integration tests | pytest and Python docs; *TPP* “Test to Code”, “Property-Based Testing” |
| 0010 Put volatile dependencies at boundaries | Isolate databases, models, clocks, and network clients | Introduce one narrow adapter | *APOSD* Chs. 5, 7–8 |
| 0011 Refactor under evidence | Improve structure without changing behaviour | Complete a tested refactoring sequence | *APOSD* Ch. 16; *TPP* “Refactoring”, “Version Control”; Git docs |

**Exit evidence:** the learner can change code structure while preserving tested behaviour and containing external dependencies.

### Module 4: Model the domain (selected)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0012 Build language from examples | Discover rules before naming abstractions | Replace vague terms with scenario-backed language | *DDD* Chs. 1–3 |
| 0013 Choose entities, values, and services deliberately | Model identity, value, and operations only where behaviour requires them | Refactor one domain rule into an explicit model | *DDD* Chs. 4–6 |
| 0014 Protect context boundaries | Stop external models leaking into the core | Add an anticorruption adapter and context map. Optional exercise: swap in a real taxonomy (e.g. ANZSIC or NAICS) behind an adapter, so the core keeps its own plain category list | *DDD* Ch. 14 |
| 0015 Distil the core | Spend design effort where differentiation lives | Separate core, supporting, and generic concerns | *DDD* Ch. 15 |

**Exit evidence:** the learner can model a real rule without overengineering a simple workflow.

### Module 5: Design data that can evolve (selected)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0016 Turn qualities into measurable requirements | Define latency, reliability, load, and maintainability targets | Write service-level indicators and budgets | *TPP* Topic 5 and Tip 8 (to verify against book); measurement: official docs |
| 0017 Choose a data model from access patterns | Match relationships and queries to the model | Compare relational, document, and graph designs | *DDD Reference* (repositories); data models: SQLite, PostgreSQL and Python docs |
| 0018 Understand storage trade-offs | Connect indexes and layout to read/write behaviour | Explain one query plan and index decision | *TPP* Topic 39, Tips 63 and 64 (to verify against book); indexes: SQLite and PostgreSQL docs |
| 0019 Evolve schemas without coordinated deployment | Preserve compatibility across versions | Run old and new readers against evolving data | Official SQLite, PostgreSQL and Python docs only; *TPP* Tip 18 and Topic 27 for small, reversible steps |
| 0020 Protect invariants under concurrency | Choose an isolation guarantee from the failure you must prevent | Reproduce and fix a transaction anomaly | *TPP* Topic 34 (free excerpt); *DDD Reference* (aggregates); isolation levels: database docs |

**Exit evidence:** the learner can justify a data decision using access patterns, compatibility, and correctness requirements.

**Source note:** none of the three main books covers this module’s design trade-offs.
Official database documentation defines behaviour, but the reasoning about requirements, data models, storage, schema evolution, and isolation needs a chosen source before these lessons are written.

### Module 6: Operate what you build (required for the capstone)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0021 Observe promises and failures | Instrument what users depend on | Add structured logs, metrics, traces, and one alert | OpenTelemetry, Python and OWASP docs only |
| 0022 Deploy reversibly | Make configuration, migration, rollout, and rollback explicit | Ship a backwards-compatible change with rollback | *TPP* “Reversibility”, “Configuration”; GitHub Actions and Git docs |
| 0023 Measure before optimizing | Locate the critical path before changing code | Benchmark, change, and compare | *APOSD* Ch. 20 |
| 0024 Design for expected failure | Choose retries, timeouts, idempotency, and fallbacks from failure semantics | Test one degraded-mode scenario | Python, SQLite and HTTP (RFC 9110) docs only; *APOSD* Ch. 10 for masking errors (to verify against book) |

**Exit evidence:** the learner can deploy and diagnose the service without guessing.

### Toolkit strand (proposed, not scheduled)

The design modules assume the learner can run commands, save and undo changes, and find bugs.
These candidate lessons fill that gap and slot in where the service first needs the skill.
They keep `T` labels until written, so existing lesson numbers do not change.

| Candidate | Durable decision | Suggested placement | Practice change | Main sources |
|---|---|---|---|---|
| T1 Work in the shell with plain text | Keep inputs, outputs, and settings in text that tools can read and repeat | Before 0009, because tests run from the command line | Run the service on a text file of company names from the terminal | *TPP* “The Power of Plain Text”, “Shell Games”; shell docs |
| T2 Save every change in version control | Make each change reviewable and reversible | Before 0011, because refactoring needs a safe undo | Commit one refactoring step at a time and revert one | *TPP* “Version Control”; Git docs |
| T3 Debug from evidence | Reproduce, isolate, and confirm a fault before fixing it | With 0008, when failures are first designed | Reproduce a failed About-page fetch, then fix and add a test | *TPP* “Debugging”; Python `pdb` docs |
| T4 Estimate and check | State an estimate with its uncertainty, then compare with the actual | Before 0016, or when planning the capstone | Estimate one service change, record the actual, and adjust | *TPP* “Estimating” |

## Progression rules

- Modules 1–3 are prerequisites for domain or distributed-system material.
- A learner may skip a lesson by demonstrating its exit evidence.
- The next lesson is selected from observed mistakes and transfer performance, not generated merely because it appears next in the table.
- Every fourth lesson should interleave an earlier skill to strengthen retention.
- Public lessons cite sources; copyrighted source files and acquisition details are never committed.
