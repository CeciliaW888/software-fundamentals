# Day 17: Choose a data model from access patterns

[← Previous: Day 16 Turn qualities into measurable requirements](./day-16-measurable-requirements.md) | [Course Home](../README.md) | [Next: Day 18 Understand storage trade-offs →](./day-18-storage-trade-offs.md)

> 📍 **Where we are in the story:** Week 3 · The model fits the business. Now the data it keeps has to evolve without breaking.

---

> **Book coverage:** Evans's *DDD Reference* covers repositories, which shape the store's interface.
> Comparing relational, document, and graph models is not in the books' freely available material, so that part relies on the official SQLite, PostgreSQL, and Python documentation.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. List the questions the service and its users will ask of stored data.
2. Design tables that answer those questions simply.
3. Compare a relational, a document, and a graph shape for the same data.
4. Store results in SQLite through an adapter the core never sees.

**Plain idea:** design storage from the questions you will ask of it, not from the objects you happen to have.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 5 · Design data that can evolve (lesson 0017)

---

## 📚 Core Concepts

### Observe: results disappear, and reviewers can't find their work

The Module 4 store keeps results in a Python list.
Two problems show up as soon as the review team uses it.
First, everything is lost when the program stops.
Second, the store only keeps *suggested* results, but the reviewers' whole job is the other kind: the companies that need review.
There is nowhere to ask "what's waiting for me?".

So before choosing a database, write down the questions, the **access patterns**:

1. Record every enrichment result, with its outcome, reason, suggestion, and evidence.
2. Get the latest result for one company.
3. List the results waiting for review, oldest first.
4. Show the full history of one company's results.

Pattern 1 changes the service's behaviour: `Enricher` now records every result, not only suggested ones.
That is a deliberate change, made because a real user need required it, and the docstring and a test say so.

### Say it plainly: shape the data for the questions

Each pattern hints at a shape.

- Patterns 2 and 4 ask "everything about one company", so results need a company ID.
- Pattern 3 asks "all results with outcome *needs review*, by time", across all companies, so outcome and time should be plain columns that can be filtered and sorted.
- Companies have a name that can change (Day 13), so they get their own small table, and results refer to them by ID.

That gives two tables: `companies` and `results`.
Each result row holds its outcome, reason, category, confidence, evidence, and the time it was checked.

Now compare other shapes for the same data:

| Shape | How it would store a result | Fits our patterns? |
|---|---|---|
| **Relational** (tables, rows, columns) | one row per result, columns for each field | yes: all four patterns are simple queries |
| **Document** (one JSON document per company) | each company's document holds a list of its results | patterns 2 and 4 are easy; pattern 3 must search inside every document |
| **Graph** (nodes and edges) | companies, categories, and results as nodes, linked by edges | strong for "which companies are related?"; nobody asks that here |

The relational shape wins, not because it is always best, but because these four questions are simple filters and sorts over one kind of record.
PostgreSQL can also store JSON inside a relational table, which is useful when part of a record has no fixed shape.

SQLite is enough for this service: it is a database in a single file, built into Python's standard library through the `sqlite3` module.
The adapter `SqliteResultStore` implements the same `save` method as the in-memory store, plus one method per access pattern.

### Name it: access patterns, schema, relational model

An **access pattern** is a question the system will repeatedly ask of its data.
A **schema** is the declared structure of a database: its tables, columns, and their types.
A **relational database** stores data as rows in tables and answers questions with SQL; SQLite and PostgreSQL are both relational.
A **primary key** is the column that identifies each row; a **foreign key** is a column whose values must match a primary key in another table.

Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) describes a **repository** as the way a model offers query access to stored objects in the ubiquitous language, so database details don't leak into the domain code.
`SqliteResultStore` plays that role: its methods are named for reviewers' questions, such as `review_queue`, and only the adapter knows about SQL.

> **Key Insight:** List the queries first. A schema that makes your most frequent queries simple is a good schema for you, whatever is fashionable.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Access pattern** | A question the system repeatedly asks of its stored data. | Course-authored plain definition |
| **Schema** | The declared structure of a database: tables, columns, and their types. | Standard database vocabulary; see [SQLite: CREATE TABLE](https://www.sqlite.org/lang_createtable.html) |
| **Relational database** | A database that stores rows in tables and is queried with SQL. | Standard database vocabulary; this plain definition is course-authored |
| **Primary key** | The column or columns that uniquely identify each row in a table. | Official SQLite vocabulary ([CREATE TABLE](https://www.sqlite.org/lang_createtable.html)) |
| **Foreign key** | A column whose values must match a key in another table. | Official SQLite vocabulary ([foreign keys](https://www.sqlite.org/foreignkeys.html)) |
| **Document model** | Storing each record as a self-contained document, such as JSON. | Standard database vocabulary; see [PostgreSQL: JSON types](https://www.postgresql.org/docs/current/datatype-json.html) |
| **Repository** | An object that gives the model query access to stored objects in the model's own language, hiding the database details. | Paraphrased from Eric Evans, *Domain-Driven Design*; concept checked in Evans's free *DDD Reference*; chapter to verify against book |

---

## 💻 Code Examples

### Example 1: The tables, shaped by the patterns

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py)*

```sql
CREATE TABLE companies (
    company_id TEXT PRIMARY KEY,
    name       TEXT NOT NULL
);
CREATE TABLE results (
    result_id        INTEGER PRIMARY KEY,
    company_id       TEXT NOT NULL REFERENCES companies (company_id),
    outcome          TEXT NOT NULL,
    reason           TEXT,
    category         TEXT,
    confidence       REAL,
    evidence_url     TEXT,
    evidence_excerpt TEXT,
    checked_at       TEXT NOT NULL
);
```

**What's happening:** every column a pattern filters or sorts on is a plain column.
Fields that only some results have, such as `reason`, allow `NULL`.

### Example 2: One method per access pattern

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/sqlite_store.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/sqlite_store.py)*

```python
def review_queue(self, limit=20):
    """Access pattern 3: results waiting for a person, oldest first."""
    return self.connection.execute(
        "SELECT * FROM results WHERE outcome = ? ORDER BY checked_at LIMIT ?",
        (Outcome.NEEDS_REVIEW.value, limit),
    ).fetchall()
```

**What's happening:** the `?` placeholders let `sqlite3` pass values safely, so data is never pasted into SQL text.

### Example 3: The behaviour change, stated

*File: [`projects/company-enricher/stages/05-design-data/tests/test_scenarios.py`](../projects/company-enricher/stages/05-design-data/tests/test_scenarios.py)*

```python
def test_every_result_is_recorded_for_reporting_or_review(enricher, store):
    suggested = enricher.enrich(company("Saltwater Kitchen"))
    needs_review = enricher.enrich(company("Lantern Lane Bakery"))
    assert store.saved_results == [suggested, needs_review]
```

**What's happening:** the old test said "only suggested results are saved". The requirement changed, so the test changed with it, on purpose.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why are `outcome` and `checked_at` plain columns?**

- A. SQLite requires every field as a column.
- B. To save disk space.
- C. The review queue filters by outcome and sorts by time across all companies.
- D. Because they never change.

<details>
<summary>Answer</summary>

**C.** Access pattern 3 needs to filter and sort on them, which is simple and fast on plain columns.

</details>

**Q2. Which access pattern is awkward for a one-document-per-company design?**

- A. The latest result for one company
- B. The history of one company
- C. Saving a result
- D. All results waiting for review, oldest first, across companies

<details>
<summary>Answer</summary>

**D.** The queue cuts across every company, so a per-company document design has to look inside all documents.

</details>

**Q3. Why does `review_queue` use `?` placeholders?**

- A. Values are passed separately from the SQL, so data cannot change the query.
- B. They make queries shorter.
- C. SQLite cannot read numbers otherwise.
- D. They sort the results.

<details>
<summary>Answer</summary>

**A.** Parameter substitution keeps data and SQL apart, which is what the Python `sqlite3` documentation recommends.

</details>

### Exercise 2 · Change: a fifth access pattern (⏱️ ~20 min)

**Goal:** Extend the model from a new question.

**Instructions:**
1. Reviewers ask: "how many companies are in each category among suggested results?".
2. Write the SQL query first, then add a method `category_counts()` to `SqliteResultStore`.
3. Write a test in `tests/test_sqlite_store.py` that enriches three companies and checks the counts.
4. Decide whether the schema needs to change. Explain why or why not.

<details>
<summary>Hint</summary>

`SELECT category, count(*) FROM results WHERE outcome = 'suggested' GROUP BY category` needs no new column.

</details>

### Exercise 3 · Transfer: list the questions (⏱️ ~10 min)

For a feature you know that stores data, list its access patterns.
Mark the one asked most often, and check whether the current schema makes it simple.

---

## 📖 Curated Resources

1. **[Python documentation: sqlite3](https://docs.python.org/3/library/sqlite3.html)**
   - Why: connections, `execute`, placeholders, and `Row` objects.
2. **[SQLite: CREATE TABLE](https://www.sqlite.org/lang_createtable.html)**
   - Why: column types, primary keys, and `NOT NULL`.
3. **[PostgreSQL: JSON types](https://www.postgresql.org/docs/current/datatype-json.html)**
   - Why: how a relational database can also hold document-shaped data.
4. **Book coverage for data-model trade-offs:** none in the three books' freely available material; official documentation only.
   - Why: a book source should be chosen when the full books are available.
5. **Free source:** Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/).
   - Why: the repository pattern in the author's own short form.

---

## 🤔 Reflection Questions

1. **Comprehension:** What is an access pattern, and why list them before the schema?
2. **Application:** If reviewers later want "companies similar to this one", which shape becomes more attractive?
3. **Connection:** How did Day 15's ports make swapping the store a one-adapter change?
4. **Critical Thinking:** What is lost by storing the category as text rather than as a reference to a categories table?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 18: Understand storage trade-offs](./day-18-storage-trade-offs.md). The review queue works; next you make sure it stays fast as results pile up.

**Before moving on, make sure you can:**

- [ ] List the four access patterns of the service.
- [ ] Explain why the relational shape fits them.
- [ ] Find each pattern's method in `SqliteResultStore`.

[← Previous: Day 16 Turn qualities into measurable requirements](./day-16-measurable-requirements.md) | [Course Home](../README.md) | [Next: Day 18 Understand storage trade-offs →](./day-18-storage-trade-offs.md)
