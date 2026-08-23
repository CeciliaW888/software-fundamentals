# Course design

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
Each tooltip shows a plain definition and its provenance.
Use a book definition only when the book actually defines the term; otherwise use official documentation, a domain authority, or label the definition as course-authored.

## One evolving practice service

The course follows one small Python customer industry-enrichment service from a readable function to an operable system.

The service:

1. receives a customer name
2. finds the customer’s official website
3. reads the website’s About page
4. summarises the business’s main activity
5. suggests an ANZSIC code and label
6. records the source text, confidence, and review status

The output is a suggestion because public website text may be incomplete or ambiguous.
The service must retain evidence and send uncertain cases to human review.

The example is generic and uses public sample data only.
It does not contain employer data, code, decision rules, or internal processes.
The service is a practice vehicle, not the course identity.
APIs, scraping, storage, queues, and deployment appear only when they create a useful software-design decision.

## Source hierarchy

### 1. Behavioural authority

Official language, standard-library, protocol, database, and tool documentation define actual behaviour.
Use these sources for syntax, semantics, compatibility, configuration, and operational guarantees.

### 2. Core design spine

John Ousterhout’s *A Philosophy of Software Design, 2nd Edition* supplies the recurring vocabulary for complexity, decomposition, deep modules, information hiding, errors, documentation, consistency, alternatives, and performance.
Its principles are hypotheses to test against code, not rules to obey mechanically.

### 3. Deliberate counterpoint

Robert C. Martin’s *Clean Code* contributes useful craftsmanship examples, especially naming, boundaries, tests, and code smells.
Where it conflicts with system-level simplicity, present both views and make the learner compare total complexity.
Function length and comments are explicit comparison topics.

### 4. Domain specialization

Eric Evans’s *Domain-Driven Design* supports selected lessons on knowledge discovery, ubiquitous language, model/code alignment, entities, value objects, services, bounded contexts, anticorruption layers, and core-domain distillation.
Do not turn its tactical patterns into a default architecture.

### 5. Data and systems specialization

*Designing Data-Intensive Applications* supports later lessons on nonfunctional requirements, data models, storage, schema evolution, transactions, replication, and sharding.
The reviewed second-edition Early Release is incomplete, so public lessons must cite a stable published edition or finalized official material.

## Curriculum

### Module 1: Read code before changing it (required)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0001 Use names that explain the job | Make the business object, stage, unit, and decision visible | Rename an opaque ANZSIC-suggestion function without changing behaviour | *APOSD* Ch. 14; *Clean Code* Ch. 2; PEP 8 |
| 0002 Know what a function promises | Separate what other code may rely on from how the work happens | Describe and test one function’s promised behaviour | *APOSD* Chs. 4, 13; PEP 257 |
| 0003 Follow the data and outside changes | Identify inputs, outputs, stored changes, and external dependencies | Trace customer name to ANZSIC suggestion and evidence | *APOSD* Chs. 2, 5 |

**Exit evidence:** the learner can explain an unfamiliar function’s job, inputs, possible results, outside changes, and failures before editing it.

### Module 2: Control complexity (required)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0004 Recognise complexity by its symptoms | Find change amplification, cognitive load, and unknown unknowns | Score one change before and after refactoring | *APOSD* Ch. 2 |
| 0005 Build deep modules | Hide useful complexity behind a small, complete interface | Replace pass-through helpers with one coherent module | *APOSD* Chs. 4–8 |
| 0006 Split by information, not length | Keep related knowledge together and independent knowledge apart | Compare a short-function design with a deep-function design | *APOSD* Ch. 9; *Clean Code* Ch. 3 |
| 0007 Design it twice | Compare alternatives before committing to structure | Produce two APIs and choose with explicit criteria | *APOSD* Ch. 11 |

**Exit evidence:** the learner can defend a module boundary using total system complexity rather than file size or style rules.

### Module 3: Change safely (required)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0008 Decide what each failure means | Prevent, hide, combine, or report errors intentionally | Redesign one website or classification failure path | *APOSD* Ch. 10; Python docs |
| 0009 Tests are executable evidence | Test promised behaviour instead of internal trivia | Add focused unit and integration tests | pytest and Python docs; selected *Clean Code* testing material |
| 0010 Put volatile dependencies at boundaries | Isolate databases, models, clocks, and network clients | Introduce one narrow adapter | *APOSD* Chs. 5, 7–8 |
| 0011 Refactor under evidence | Improve structure without changing behaviour | Complete a tested refactoring sequence | *APOSD* Ch. 16 |

**Exit evidence:** the learner can change code structure while preserving tested behaviour and containing external dependencies.

### Module 4: Model the domain (selected)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0012 Build language from examples | Discover rules before naming abstractions | Replace vague terms with scenario-backed language | *DDD* Chs. 1–3 |
| 0013 Choose entities, values, and services deliberately | Model identity, value, and operations only where behaviour requires them | Refactor one domain rule into an explicit model | *DDD* Chs. 4–6 |
| 0014 Protect context boundaries | Stop external models leaking into the core | Add an anticorruption adapter and context map | *DDD* Ch. 14 |
| 0015 Distil the core | Spend design effort where differentiation lives | Separate core, supporting, and generic concerns | *DDD* Ch. 15 |

**Exit evidence:** the learner can model a real rule without overengineering a simple workflow.

### Module 5: Design data that can evolve (selected)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0016 Turn qualities into measurable requirements | Define latency, reliability, load, and maintainability targets | Write service-level indicators and budgets | *DDIA* Ch. 2 |
| 0017 Choose a data model from access patterns | Match relationships and queries to the model | Compare relational, document, and graph designs | *DDIA* Ch. 3 |
| 0018 Understand storage trade-offs | Connect indexes and layout to read/write behaviour | Explain one query plan and index decision | *DDIA* Ch. 4; database docs |
| 0019 Evolve schemas without coordinated deployment | Preserve compatibility across versions | Run old and new readers against evolving data | *DDIA* Ch. 5 |
| 0020 Protect invariants under concurrency | Choose an isolation guarantee from the failure you must prevent | Reproduce and fix a transaction anomaly | *DDIA* Ch. 8; database docs |

**Exit evidence:** the learner can justify a data decision using access patterns, compatibility, and correctness requirements.

### Module 6: Operate what you build (required for the capstone)

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0021 Observe promises and failures | Instrument what users depend on | Add structured logs, metrics, traces, and one alert | OpenTelemetry and platform docs; *DDIA* Ch. 2 |
| 0022 Deploy reversibly | Make configuration, migration, rollout, and rollback explicit | Ship a backwards-compatible change with rollback | Platform and database docs |
| 0023 Measure before optimizing | Locate the critical path before changing code | Benchmark, change, and compare | *APOSD* Ch. 20; *DDIA* Ch. 2 |
| 0024 Design for expected failure | Choose retries, timeouts, idempotency, and fallbacks from failure semantics | Test one degraded-mode scenario | Protocol and platform docs; selected *DDIA* chapters |

**Exit evidence:** the learner can deploy and diagnose the service without guessing.

## Progression rules

- Modules 1–3 are prerequisites for domain or distributed-system material.
- A learner may skip a lesson by demonstrating its exit evidence.
- The next lesson is selected from observed mistakes and transfer performance, not generated merely because it appears next in the table.
- Every fourth lesson should interleave an earlier skill to strengthen retention.
- Public lessons cite sources; copyrighted source files and acquisition details are never committed.
