# Software Fundamentals resources

## Source policy

Sources have different jobs.
Official documentation defines behaviour.
Books provide design lenses.
Domain authorities define business classifications.
No source is treated as a universal rulebook.

Each lesson labels unfamiliar words as one of:

- official Python vocabulary
- standard software-engineering vocabulary
- a named author’s term
- domain language for this service
- course-authored shorthand

## Behavioural and domain authority

- [Python documentation](https://docs.python.org/3/) for language and standard-library behaviour
- [Python glossary](https://docs.python.org/3/glossary.html) for Python-specific vocabulary
- [PEP 8](https://peps.python.org/pep-0008/) for Python naming and readability conventions
- [PEP 257](https://peps.python.org/pep-0257/) for Python docstring conventions
- [pytest documentation](https://docs.pytest.org/) for tests and failure feedback
- [Australian and New Zealand Standard Industrial Classification, 2006 Revision 2.0](https://www.abs.gov.au/statistics/classifications/australian-and-new-zealand-standard-industrial-classification-anzsic/latest-release) for ANZSIC structure, definitions, and coding guidance
- [FastAPI documentation](https://fastapi.tiangolo.com/) when an HTTP boundary is introduced
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) when monitoring is introduced
- Database and deployment-platform documentation for product-specific guarantees

ANZSIC is jointly developed by the Australian Bureau of Statistics and Stats NZ for compiling and analysing industry statistics.
A website-based result in this course is therefore called a **suggestion**, not an authoritative classification.
The service retains evidence, confidence, and review status.

## Core design spine

### *A Philosophy of Software Design, 2nd Edition* by John Ousterhout

**Role:** primary source for software design and refactoring judgment.

Use for complexity, modules, information hiding, errors, design alternatives, comments, naming, consistency, modifying code, and performance.
The author’s principles are tested against code rather than followed mechanically.

- [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)

## Deliberate counterpoint

### *Clean Code* by Robert C. Martin

**Role:** selected craftsmanship source and debate partner, not the course spine.

Use for intention-revealing names, boundaries, tests, and code smells.
Contrast its preference for very small functions and restrained comments with Ousterhout’s emphasis on deep modules, total complexity, and useful interface documentation.

- [Publisher page](https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship/P200000009044/9780136083238)

## Domain specialization

### *Domain-Driven Design: Tackling Complexity in the Heart of Software* by Eric Evans

**Role:** source for selected domain-modeling lessons.

Use for learning the business problem, domain-specific shared language, model and code alignment, entities, value objects, services, context boundaries, and core-domain focus.
Do not treat its Java examples or tactical patterns as a default architecture.

In this course, terms such as **customer**, **official website**, **About page**, **industry evidence**, **ANZSIC suggestion**, and **review required** may become domain language when their meanings are agreed.
Technical terms such as **function**, **exception**, and **return value** are not domain language.

- [Official DDD resources](https://www.domainlanguage.com/ddd/)

## Data and systems specialization

### *Designing Data-Intensive Applications* by Martin Kleppmann; second edition with Chris Riccomini

**Role:** advanced source for data and systems trade-offs.

Use later for reliability, scalability, maintainability, data models, storage, schema evolution, transactions, replication, and sharding.
The reviewed second-edition Early Release is incomplete, so public lessons cite stable published or finalized official material.

- [Official DDIA site](https://dataintensive.net/)

## Known source gaps

Before publishing the relevant modules, select stable primary sources for:

- secure software design and threat modeling
- deployment, migration, and rollback
- production incident response
- accessibility for developer-facing and user-facing interfaces
