# Software Fundamentals

A public, practice-led course for learning how to understand, design, test, and change reliable software.

The course assumes **no software-engineering background**.
Plain words and observable behaviour come first.
Technical terms appear only after the idea is concrete, and each term is labelled by its source.

## The one service used throughout

Every lesson improves the same small Python **customer industry-enrichment service**:

1. Receive a customer name.
2. Find the customer’s official website.
3. Read the website’s About page.
4. Summarise the business’s main activity.
5. Suggest a code and label from the Australian and New Zealand Standard Industrial Classification (ANZSIC).
6. Keep the evidence, source page, confidence, and review status.

The service suggests a classification; it does not pretend that website text is always enough for an authoritative decision.
Low-confidence or ambiguous cases go to human review.

This one example will grow gradually as the course introduces functions, tests, storage, errors, data models, external services, deployment, and monitoring.

## Start here

- [Mission](MISSION.md)
- [Course design and curriculum](COURSE_DESIGN.md)
- [Source hierarchy](RESOURCES.md)
- [Lesson 0001: Use names that explain the job](lessons/0001-names-are-architecture.html)
- [Lesson 0002: Know what a function promises](lessons/0002-read-contracts-before-bodies.html)
- [Reference: Meaningful names for Python systems](reference/meaningful-python-names.html)
- [Reference: What a Python function promises](reference/python-interface-contracts.html)

## Learning path

1. **Read code before changing it:** names, function promises, data movement, outside changes
2. **Control complexity:** decomposition, deep modules, information hiding, design alternatives
3. **Change safely:** errors, tests, boundaries, refactoring
4. **Model the business problem:** shared domain language, value objects, context boundaries
5. **Design data that can evolve:** access patterns, schemas, storage, transactions
6. **Operate what you build:** reliability, observability, performance, deployment and rollback

The first three modules form the required core.
Later ideas appear only when the customer-enrichment service creates a real need for them.

## Source policy

No single book is treated as law.

- Official Python, ABS, and tool documentation define behaviour and classifications.
- *A Philosophy of Software Design* is the main design spine.
- *Clean Code* is an influential counterpoint.
- *Domain-Driven Design* supports selected business-language and modeling lessons.
- *Designing Data-Intensive Applications* supports later data and systems lessons.

See [RESOURCES.md](RESOURCES.md) for exact roles and edition caveats.

## Course status

Lessons 0001 and 0002 are live.
The curriculum is a tested sequence of learning goals, not a promise to generate every lesson before learner evidence supports it.
