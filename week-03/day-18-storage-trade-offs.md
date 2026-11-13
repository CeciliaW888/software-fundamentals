# Day 18: Understand storage trade-offs

[← Previous: Day 17 Choose a data model from access patterns](./day-17-data-model-from-access.md) | [Course Home](../README.md) | [Next: Day 19 Evolve schemas without coordinated deployment →](./day-19-evolve-schemas.md)

> 📍 **Where we are in the story:** Week 3 · The model fits the business. Now the data it keeps has to evolve without breaking.

---

> **Book coverage:** *The Pragmatic Programmer*'s algorithm-speed tips (Tips 63 and 64 in the official tip list) give the reasoning about growth.
> Indexes and query plans themselves are not in the books' freely available material, so those parts rely on the official SQLite and PostgreSQL documentation.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Read a query plan and tell a full table scan from an index search.
2. Choose an index from an access pattern's filter and sort.
3. Explain what an index costs as well as what it saves.
4. Pin a query plan in a test so a schema change cannot silently slow a query.

**Plain idea:** an index is a sorted shortcut to the rows you ask for most; it speeds up those reads and makes every write do a little more work.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 5 · Design data that can evolve (lesson 0018)

---

## 📚 Core Concepts

### Observe: ask the database how it will answer

The review queue query is:

```text
SELECT * FROM results WHERE outcome = ? ORDER BY checked_at LIMIT ?
```

With a dozen sample rows it is instant.
With a year of results it might not be.
Instead of guessing, ask the database: in SQLite, putting `EXPLAIN QUERY PLAN` in front of a query returns the plan it would use, without running it.

On the Day 17 schema, the plan says `SCAN results`, plus a step that sorts the matching rows by time.
**Scan** means SQLite will read every row in the table, check each one's outcome, then sort the matches.
The work grows with the size of the whole table, not with the size of the queue.

### Say it plainly: a sorted shortcut, with a cost

An index is a separate, sorted copy of some columns, with a pointer back to each row.
The review queue filters on `outcome` and sorts on `checked_at`, so an index on `(outcome, checked_at)` stores exactly what the query needs, in exactly the order it needs it.

After migration 2 adds that index, the plan becomes:

`SEARCH results USING INDEX results_review_queue (outcome=?)`

**Search** means SQLite jumps straight to the *needs review* entries, already in time order, and stops after `LIMIT` rows.
No full scan, and no separate sort.

Indexes are not free:

| Cost | Why |
|---|---|
| Slower writes | every insert must also update the index |
| More storage | the index is a second copy of those columns |
| Something to maintain | the planner only uses it if the query matches its columns |

So you add an index for a frequent, important query, not for every column.
The review queue is the reviewers' main screen, which earns it an index; nobody yet sorts results by confidence, so that column gets none.

The project's test `test_query_plan.py` checks both plans: a scan without the index, a search with it.
If someone later changes the query or drops the index, the test fails instead of the screen quietly getting slower.

### Name it: index, query planner, scan, search

A database's **query planner** chooses how to execute each query.
A **full table scan** reads every row; an **index search** uses an index to find matching rows directly.
A **composite index** covers more than one column, and its column order matters: SQLite's documentation explains that the planner can use the leftmost columns of an index for equality tests and the next column for sorting.

PostgreSQL works the same way in principle, with its own `EXPLAIN` command and plan format, and documents several index types beyond the default.

*The Pragmatic Programmer*'s Topic 39, "Algorithm Speed" (to verify against book), gives the reasoning behind the index: a scan's work grows in step with the table, while an index lookup grows far more slowly.
Its Tips 63 (p. 207), "Estimate the Order of Your Algorithms", and 64 (p. 208), "Test Your Estimates", in the publisher's [official list of the book's tips](https://pragprog.com/tips/), are the two halves of this lesson: reason about growth, then check with the query plan.

> **Key Insight:** Don't guess where time goes in a query; ask the planner, add the index the plan needs, and pin the plan in a test.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Index** | A separate sorted structure that lets the database find rows by some columns without reading the whole table. | Official SQLite vocabulary ([CREATE INDEX](https://www.sqlite.org/lang_createindex.html)) |
| **Query plan** | The steps the database will take to answer a query. | Official SQLite vocabulary ([EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)) |
| **Query planner** | The part of the database that chooses a query plan. | Official SQLite vocabulary ([query planning](https://www.sqlite.org/queryplanner.html)) |
| **Full table scan** | Reading every row of a table to answer a query. | Standard database vocabulary; this plain definition is course-authored |
| **Composite index** | An index on more than one column, used left to right. | Standard database vocabulary; see [SQLite query planning](https://www.sqlite.org/queryplanner.html) |
| **Write amplification** | Extra work each write must do, such as updating indexes. | Standard database vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: The index, as a migration

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py)*

```sql
CREATE INDEX results_review_queue
    ON results (outcome, checked_at);
```

**What's happening:** column order follows the query: filter by `outcome` first, then read in `checked_at` order.

### Example 2: Asking for the plan

*File: [`projects/company-enricher/stages/05-design-data/tests/test_query_plan.py`](../projects/company-enricher/stages/05-design-data/tests/test_query_plan.py)*

```python
def plan(connection):
    rows = connection.execute("EXPLAIN QUERY PLAN " + QUEUE_QUERY, ("needs_review", 20)).fetchall()
    return " | ".join(row[-1] for row in rows)
```

**What's happening:** the last column of each plan row is SQLite's description of that step.

### Example 3: Pinning both plans

*File: [`projects/company-enricher/stages/05-design-data/tests/test_query_plan.py`](../projects/company-enricher/stages/05-design-data/tests/test_query_plan.py)*

```python
def test_without_the_index_the_queue_query_scans_every_row():
    connection = sqlite3.connect(":memory:")
    migrate(connection, target=1)
    assert "SCAN results" in plan(connection)


def test_with_the_index_the_queue_query_searches_it():
    connection = sqlite3.connect(":memory:")
    migrate(connection, target=len(MIGRATIONS))
    assert "SEARCH results USING INDEX results_review_queue (outcome=?)" in plan(connection)
```

**What's happening:** the first test proves the index is what makes the difference; the second guards it.

> **💡 Try it:** run `sqlite3 :memory:` in a terminal, paste the Day 17 tables, and type `EXPLAIN QUERY PLAN SELECT * FROM results WHERE outcome = 'needs_review' ORDER BY checked_at;`. Then add the index and run it again.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. What does `SCAN results` in a plan mean?**

- A. SQLite uses an index.
- B. SQLite reads every row in the table.
- C. The query failed.
- D. The table is empty.

<details>
<summary>Answer</summary>

**B.** A scan reads the whole table. With an index the plan says SEARCH ... USING INDEX.

</details>

**Q2. Why is the index on `(outcome, checked_at)` and not `(checked_at, outcome)`?**

- A. Alphabetical order
- B. SQLite only allows that order
- C. The query filters by outcome, then sorts by time, and indexes are used left to right
- D. It uses less space

<details>
<summary>Answer</summary>

**C.** The leftmost column serves the equality filter; the next one provides the order, so no separate sort is needed.

</details>

**Q3. What is the main cost of adding an index?**

- A. Reads become slower.
- B. The table can no longer be queried.
- C. SQL becomes longer.
- D. Every write must also update the index, and it takes space.

<details>
<summary>Answer</summary>

**D.** Indexes speed up matching reads at the cost of extra work on every write and extra storage.

</details>

### Exercise 2 · Change: index the history query (⏱️ ~20 min)

**Goal:** Decide on an index from a plan, not a guess.

**Instructions:**
1. Write a test like `plan()` for the history query: `SELECT * FROM results WHERE company_id = ? ORDER BY checked_at, result_id`.
2. Run it against the current schema and read the plan.
3. Decide whether an index on `(company_id, checked_at)` is worth it, given how often reviewers open a company's history.
4. If yes, add it as a new migration (never edit an old one) and update the test to expect a search.

<details>
<summary>Hint</summary>

Append a new SQL string to `MIGRATIONS`. Day 19 explains why released migrations are never edited.

</details>

### Exercise 3 · Transfer: read one plan (⏱️ ~10 min)

In any database you use, run `EXPLAIN` (PostgreSQL) or `EXPLAIN QUERY PLAN` (SQLite) on one frequent query.
Write down whether it scans or searches, and which index it uses.

---

## 📖 Curated Resources

1. **[SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)**
   - Why: how to read SQLite's plan output.
2. **[SQLite: The SQLite Query Optimizer Overview](https://www.sqlite.org/optoverview.html)**
   - Why: when the planner can use an index, including for `ORDER BY`.
3. **[SQLite: Query Planning](https://www.sqlite.org/queryplanner.html)**
   - Why: a plain explanation of how indexes and multi-column indexes work.
4. **[PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)** and **[Indexes](https://www.postgresql.org/docs/current/indexes.html)**
   - Why: the same ideas in PostgreSQL.
5. **Book coverage for indexes and query plans:** none in the three books' freely available material; official documentation only.
   - Why: a book source should be chosen when the full books are available.
6. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 39, "Algorithm Speed" (to verify against book).
   - 🔗 [Official tip list](https://pragprog.com/tips/)
   - Why: Tips 63 and 64, on estimating growth and testing the estimate.

---

## 🤔 Reflection Questions

1. **Comprehension:** In your own words, what does an index trade, and for what?
2. **Application:** The service writes far more results than reviewers read. Does that change your view of the review-queue index?
3. **Connection:** How does Day 16's latency target turn "is this index worth it?" into a measurable question?
4. **Critical Thinking:** Why might a test that pins a query plan break when you upgrade the database, and is that a good or bad thing?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 19: Evolve schemas without coordinated deployment](./day-19-evolve-schemas.md). The index arrived as migration 2; next you learn how schema changes ship safely.

**Before moving on, make sure you can:**

- [ ] Read a SQLite query plan.
- [ ] Choose a composite index from a query's filter and sort.
- [ ] Explain what an index costs.

[← Previous: Day 17 Choose a data model from access patterns](./day-17-data-model-from-access.md) | [Course Home](../README.md) | [Next: Day 19 Evolve schemas without coordinated deployment →](./day-19-evolve-schemas.md)
