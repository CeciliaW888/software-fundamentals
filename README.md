# Software Fundamentals

A public, practice-led course for learning how to understand, design, test, and evolve reliable software.

The course improves one small Python document-processing service over time.
Every lesson makes one observable change, checks understanding immediately, and transfers the idea to a real code-review decision.

## Start here

- [Mission](MISSION.md)
- [Course design and curriculum](COURSE_DESIGN.md)
- [Source hierarchy](RESOURCES.md)
- [Lesson 0001: Names are architecture in miniature](lessons/0001-names-are-architecture.html)
- [Lesson 0002: Read contracts before bodies](lessons/0002-read-contracts-before-bodies.html)
- [Reference: Meaningful names for Python systems](reference/meaningful-python-names.html)
- [Reference: Python interface contracts](reference/python-interface-contracts.html)

## Learning path

1. **Read before changing:** names, contracts, data flow, side effects
2. **Control complexity:** decomposition, deep modules, information hiding, design alternatives
3. **Change safely:** errors, tests, boundaries, refactoring
4. **Model the domain:** shared language, value objects, context boundaries
5. **Design data that can evolve:** access patterns, schemas, storage, transactions
6. **Operate what you build:** reliability, observability, performance, deployment and rollback

The first three modules form the required core.
Domain and data modules begin only after the service is understandable and safely changeable.
Distributed-system material is introduced when a concrete requirement justifies it, not as architecture theatre.

## Source policy

No single book is treated as law.

- *A Philosophy of Software Design* is the main design spine.
- Official Python and tool documentation define language and runtime behaviour.
- *Clean Code* is an influential counterpoint, especially where its rules conflict with system-level simplicity.
- *Domain-Driven Design* supports selected domain-modeling lessons.
- *Designing Data-Intensive Applications* supports later data and systems lessons.

See [RESOURCES.md](RESOURCES.md) for exact roles and edition caveats.

## Course status

Lessons 0001 and 0002 are live.
The curriculum is a tested sequence of learning goals, not a promise to generate every lesson before learner evidence supports it.
