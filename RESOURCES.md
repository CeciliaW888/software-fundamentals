# Software Fundamentals resources

## Source policy

Sources have different jobs.
Official documentation defines behaviour.
Books provide design lenses.
Communities contribute experience and disagreement.
No source is treated as a universal rulebook.

## Core design spine

### *A Philosophy of Software Design, 2nd Edition* — John Ousterhout

**Role:** primary source for software design and refactoring judgment.

Use for complexity, strategic programming, deep modules, information hiding, general-purpose interfaces, errors, design alternatives, comments, naming, consistency, modifying code, and performance.
The author explicitly recommends applying the ideas through code review and warns against taking any principle too far.

- [Official book page](https://web.stanford.edu/~ouster/cgi-bin/book.php)

## Deliberate counterpoint

### *Clean Code* — Robert C. Martin

**Role:** selected craftsmanship source and debate partner, not the course spine.

Use for intention-revealing names, boundaries, tests, and code smells.
Contrast its preferences for very small functions and restrained comments with Ousterhout’s emphasis on deep modules, total complexity, and interface documentation.

- [Publisher page](https://www.pearson.com/en-us/subject-catalog/p/clean-code-a-handbook-of-agile-software-craftsmanship/P200000009044/9780136083238)

## Domain specialization

### *Domain-Driven Design: Tackling Complexity in the Heart of Software* — Eric Evans

**Role:** canonical conceptual source for selected domain-modeling lessons.

Use Chapters 1–6, 10, 14, and 15 for knowledge discovery, ubiquitous language, model/code alignment, entities, value objects, services, intention-revealing interfaces, bounded contexts, anticorruption layers, and core-domain distillation.
Do not use its Java/UML orientation or tactical patterns as a default architecture.

- [Official DDD resources](https://www.domainlanguage.com/ddd/)

## Data and systems specialization

### *Designing Data-Intensive Applications* — Martin Kleppmann; second edition with Chris Riccomini

**Role:** advanced conceptual source for data and systems trade-offs.

Use for nonfunctional requirements, reliability, scalability, maintainability, data models, storage, encoding and schema evolution, transactions, replication, and sharding.
The available second-edition Early Release is incomplete: only Chapters 1–8 are present and later chapters are marked unavailable.
Public lessons should cite a stable published edition or finalized official material rather than the unfinished file.

- [Official DDIA site](https://dataintensive.net/)

## Behavioural authority

- [Python documentation](https://docs.python.org/3/) for language and standard-library behaviour
- [PEP 8](https://peps.python.org/pep-0008/) for Python naming and readability conventions
- [pytest documentation](https://docs.pytest.org/) for test collection, fixtures, parametrization, and failure feedback
- [FastAPI documentation](https://fastapi.tiangolo.com/) when an HTTP boundary is introduced
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) when observability is introduced
- Database and deployment-platform documentation for guarantees that depend on a chosen product

## Wisdom and external feedback

- [Python Discourse](https://discuss.python.org/) for language and ecosystem discussion
- Real code review, incident reports, and design retrospectives for testing principles against experience

## Known source gaps

Before publishing the relevant modules, select stable primary sources for:

- secure software design and threat modeling
- deployment, migration, and rollback
- production incident response
- accessibility for developer-facing and user-facing interfaces
