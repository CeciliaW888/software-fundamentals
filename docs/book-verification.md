# Book verification

The course cites three books: *A Philosophy of Software Design* (APOSD, 2nd edition), *The Pragmatic Programmer* (TPP, 20th Anniversary Edition), and *Domain-Driven Design* (DDD).
On 2026-11-14 every book citation in the lessons and website modules was checked against the full text of all three books.
Never commit the books or text taken from them: the repository and site are public.

## What was checked

- Every chapter number and chapter title cited from APOSD and DDD.
- Every topic number and topic title cited from TPP.
- Every claim a lesson attributes to a chapter or topic, including the paraphrased definitions in the Key Terminology tables and the tooltips built from them.
- Every TPP tip number and title, which had already been checked against the publisher's [official tip list](https://pragprog.com/tips/).

## What changed

- **Day 23, critical path.**
  The lesson used "critical path" for the part of a program where most time is spent.
  In APOSD Chapter 20 the critical path is the minimum code that must run in the most common case, and it matters only when no fundamental fix, such as a cache, exists.
  The lesson now calls the slow place a **bottleneck** (course-authored vocabulary), defines the critical path as Ousterhout does, and notes that a cache is his own example of a fundamental fix.
- **Day 1, service.**
  APOSD Chapter 4 does not define "service"; it lists services as one form a module can take.
  The term is now marked as standard vocabulary, with that note.
- **Day 17, repository.**
  The source is now DDD Chapter 6, "The Life Cycle of a Domain Object", instead of the free *DDD Reference* alone.

All other citations were correct as written.

## Coverage the full books added

Some lessons had said a topic was "not covered in the books' freely available material".
Searching the full books found:

- **Day 17:** DDD Chapter 6, section "Designing Objects for Relational Databases": keep tables close to the model and keep other programs from writing to an object store directly.
- **Day 19:** the same section: data migration problems discourage schema changes, and a model and schema that drift apart become hard to follow.
- **Day 20:** DDD Chapter 6's purchase-order example of two concurrent edits that are each valid but together break a rule about the whole aggregate.
- **Day 21:** TPP Topic 20, "Debugging", on tracing messages in a consistent format that tools can process.
- **Day 24:** APOSD Chapter 10's NFS example of retrying in one low layer instead of making every caller handle the failure.

## Topics the three books do not cover

These parts rely on official documentation only:

- Day 16: how to measure quality (indicators, targets, percentiles).
- Day 17: comparing relational, document, and graph data models.
- Day 18: indexes and query plans.
- Day 19: migration mechanics.
- Day 20: database isolation levels.
- Day 21: metrics and alerting.
- Day 24: timeouts, backoff, and idempotency.
