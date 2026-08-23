# Course design

## Teaching model

The course follows one evolving Python document-processing service from a readable function to an operable system.
Each lesson uses the same loop:

1. **Observe:** read a small piece of code or system behaviour.
2. **Predict:** retrieve the principle before seeing the explanation.
3. **Change:** make one constrained improvement.
4. **Check:** receive immediate, concrete feedback.
5. **Transfer:** apply the decision to a different example or real review.

The service is a practice vehicle, not the course identity.
Classification, APIs, storage, queues, and deployment appear only when they create a useful software-design decision.

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

### Module 1: Read before changing — required

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0001 Names are architecture in miniature | Make domain, stage, unit, and decision visible | Rename an opaque classifier without changing behaviour | *APOSD* Ch. 14; *Clean Code* Ch. 2; PEP 8 |
| 0002 Read contracts before bodies | Separate what a module promises from how it works | Write and test an interface contract | *APOSD* Chs. 4, 13; Python docs |
| 0003 Trace data and side effects | Identify hidden inputs, outputs, mutations, and dependencies | Draw and verify one request path | *APOSD* Chs. 2, 5 |

**Exit evidence:** the learner can explain an unfamiliar function’s meaning and change surface before editing it.

### Module 2: Control complexity — required

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0004 Recognise complexity by its symptoms | Find change amplification, cognitive load, and unknown unknowns | Score one change before and after refactoring | *APOSD* Ch. 2 |
| 0005 Build deep modules | Hide useful complexity behind a small, complete interface | Replace pass-through helpers with one coherent module | *APOSD* Chs. 4–8 |
| 0006 Split by information, not length | Keep related knowledge together and independent knowledge apart | Compare a short-function design with a deep-function design | *APOSD* Ch. 9; *Clean Code* Ch. 3 |
| 0007 Design it twice | Compare alternatives before committing to structure | Produce two APIs and choose with explicit criteria | *APOSD* Ch. 11 |

**Exit evidence:** the learner can defend a module boundary using total system complexity rather than file size or style rules.

### Module 3: Change safely — required

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0008 Make errors part of the contract | Prevent, mask, aggregate, or expose errors intentionally | Redesign one failure path | *APOSD* Ch. 10; Python docs |
| 0009 Tests are executable evidence | Test observable contracts instead of implementation trivia | Add focused unit and integration tests | pytest and Python docs; selected *Clean Code* testing material |
| 0010 Put volatile dependencies at boundaries | Isolate databases, models, clocks, and network clients | Introduce one narrow adapter | *APOSD* Chs. 5, 7–8 |
| 0011 Refactor under evidence | Improve structure without changing behaviour | Complete a tested refactoring sequence | *APOSD* Ch. 16 |

**Exit evidence:** the learner can make a structural change while preserving a tested contract and containing external dependencies.

### Module 4: Model the domain — selected

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0012 Build language from examples | Discover rules before naming abstractions | Replace vague terms with scenario-backed language | *DDD* Chs. 1–3 |
| 0013 Choose entities, values, and services deliberately | Model identity, value, and operations only where behaviour requires them | Refactor one domain rule into an explicit model | *DDD* Chs. 4–6 |
| 0014 Protect context boundaries | Stop external models leaking into the core | Add an anticorruption adapter and context map | *DDD* Ch. 14 |
| 0015 Distil the core | Spend design effort where differentiation lives | Separate core, supporting, and generic concerns | *DDD* Ch. 15 |

**Exit evidence:** the learner can model a real rule without overengineering a simple workflow.

### Module 5: Design data that can evolve — selected

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0016 Turn qualities into measurable requirements | Define latency, reliability, load, and maintainability targets | Write service-level indicators and budgets | *DDIA* Ch. 2 |
| 0017 Choose a data model from access patterns | Match relationships and queries to the model | Compare relational, document, and graph designs | *DDIA* Ch. 3 |
| 0018 Understand storage trade-offs | Connect indexes and layout to read/write behaviour | Explain one query plan and index decision | *DDIA* Ch. 4; database docs |
| 0019 Evolve schemas without coordinated deployment | Preserve compatibility across versions | Run old and new readers against evolving data | *DDIA* Ch. 5 |
| 0020 Protect invariants under concurrency | Choose an isolation guarantee from the failure you must prevent | Reproduce and fix a transaction anomaly | *DDIA* Ch. 8; database docs |

**Exit evidence:** the learner can justify a data decision using access patterns, compatibility, and correctness requirements.

### Module 6: Operate what you build — required for the capstone

| Lesson | Durable decision | Practice change | Main sources |
|---|---|---|---|
| 0021 Observe contracts and failures | Instrument what users depend on | Add structured logs, metrics, traces, and one alert | OpenTelemetry and platform docs; *DDIA* Ch. 2 |
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
