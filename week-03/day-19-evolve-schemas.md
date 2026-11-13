# Day 19: Evolve schemas without coordinated deployment

[← Previous: Day 18 Understand storage trade-offs](./day-18-storage-trade-offs.md) | [Course Home](../README.md) | [Next: Day 20 Protect invariants under concurrency →](./day-20-invariants-under-concurrency.md)

> 📍 **Where we are in the story:** Week 3 · The model fits the business. Now the data it keeps has to evolve without breaking.

---

> **Book coverage:** Schema evolution and migrations are not covered in the three books' freely available material.
> *The Pragmatic Programmer* supplies only the attitude of small, reversible steps; the mechanics rely on the official SQLite, PostgreSQL, and Python documentation.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Number schema changes as migrations and apply them in order.
2. Record which migrations a database has with SQLite's `user_version`.
3. Make an expand-only change that old code can ignore.
4. Test that old readers and new readers both work on an upgraded database.

**Plain idea:** change a live database in small, numbered steps, each one safe for the code that is already running.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 5 · Design data that can evolve (lesson 0019)

---

## 📚 Core Concepts

### Observe: a column the reviewers want

Reviewers ask a new question: "which version of the classifier made this suggestion?".
When the keywords change, they want to know which old results were made with the old keywords.
That needs a new column, `classifier_version`.

A database in use already has rows, and possibly more than one program reading it: the enrichment batch, a reviewer screen, a weekly report.
They are not all deployed at the same moment.
For a while, old code and new code run against the same database.

If the change renames or removes a column, the old programs break the moment it lands.
If it only *adds* something that old programs never ask for, they keep working.

### Say it plainly: numbered steps, expand before contract

The project keeps every schema change in one list, `MIGRATIONS`, in order.
Step 1 is the Day 17 tables; step 2 is the Day 18 index; step 3 adds the new column.
The database remembers how many steps it has applied, and `migrate()` applies only the ones after that.
Running it twice changes nothing.

Two rules keep this safe:

1. **Never edit a released step.** Some databases already ran it. Fix mistakes with a new step.
2. **Expand first, contract later.** Add new columns or tables in one release (expand). Remove or rename old ones only in a later release, once no running code uses them (contract).

Step 3 is expand-only: `ALTER TABLE results ADD COLUMN classifier_version TEXT`.
The column allows `NULL`, so rows written before it existed are still valid.
The old reader, which names its columns explicitly, never notices.
The new reader handles the old rows by treating `NULL` as `'unknown'`.

A reader that uses `SELECT *` and expects an exact number of columns would break here.
Naming columns explicitly is part of making evolution safe.

### Name it: migrations, user_version, expand and contract

A **migration** is one numbered, ordered change to a database schema.
SQLite stores a free integer in each database file, read and written with `PRAGMA user_version`, which this project uses as the migration number.
SQLite's `ALTER TABLE ... ADD COLUMN` adds a column to an existing table; its documentation lists the restrictions, such as the new column not being allowed a primary key.

**Expand and contract** is a common name for doing compatible changes first and removing the old shape later.
PostgreSQL documents the same kinds of `ALTER TABLE` operations, and the same rule applies there.

The books do not cover database migrations, but *The Pragmatic Programmer* supplies the attitude behind expand and contract.
Its Tip 18 (p. 48 in the publisher's [official list of the book's tips](https://pragprog.com/tips/)) is "There Are No Final Decisions", and Topic 27, "Don't Outrun Your Headlights", available as the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), argues for small steps whose effects you can check before taking the next.
Each migration is one such step, and expand-only steps keep the previous version runnable.

> **Key Insight:** A schema change is safe when the code already running cannot tell it happened.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Migration** | One numbered, ordered change to a database schema. | Standard software vocabulary; this plain definition is course-authored |
| **user_version** | An integer stored in a SQLite database file that applications may use as a version number. | Official SQLite vocabulary ([PRAGMA user_version](https://www.sqlite.org/pragma.html#pragma_user_version)) |
| **ALTER TABLE** | The SQL command that changes an existing table, for example by adding a column. | Official SQLite vocabulary ([ALTER TABLE](https://www.sqlite.org/lang_altertable.html)) |
| **Expand and contract** | Making only additive changes first, and removing old structures in a later release. | Standard software vocabulary; this plain definition is course-authored |
| **Backward compatible** | A change that existing code keeps working with. | Standard software vocabulary; this plain definition is course-authored |
| **Idempotent** | Giving the same result whether it runs once or many times. | Standard software vocabulary; this plain definition is course-authored |

---

## 💻 Code Examples

### Example 1: An expand-only step

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py)*

```sql
ALTER TABLE results ADD COLUMN classifier_version TEXT;
```

### Example 2: Applying only what is missing

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py)*

```python
def schema_version(connection):
    return connection.execute("PRAGMA user_version").fetchone()[0]


def migrate(connection, target=len(MIGRATIONS)):
    """Apply every step between the database's version and target."""
    current = schema_version(connection)
    for version in range(current + 1, target + 1):
        with connection:
            connection.executescript(MIGRATIONS[version - 1])
            connection.execute(f"PRAGMA user_version = {version}")
```

**What's happening:** each step and its version bump happen together, so a database is never left half-way through a step without knowing it.

### Example 3: Old and new readers, tested together

*File: [`projects/company-enricher/stages/05-design-data/tests/test_migrations.py`](../projects/company-enricher/stages/05-design-data/tests/test_migrations.py)*

```python
OLD_READER = "SELECT company_id, outcome, category FROM results"
NEW_READER = "SELECT company_id, coalesce(classifier_version, 'unknown') AS version FROM results"
```

*File: [`projects/company-enricher/stages/05-design-data/tests/test_migrations.py`](../projects/company-enricher/stages/05-design-data/tests/test_migrations.py)*

```python
def test_old_reader_still_works_after_the_new_column_is_added():
    connection = database_at_version_2_with_one_row()
    migrate(connection)
    assert connection.execute(OLD_READER).fetchall() == [("c1", "suggested", "Food & Hospitality")]


def test_new_reader_handles_rows_written_before_the_column_existed():
    connection = database_at_version_2_with_one_row()
    migrate(connection)
    assert connection.execute(NEW_READER).fetchall() == [("c1", "unknown")]
```

**What's happening:** the tests build a database as it looked before step 3, with a real row in it, then upgrade it and run both readers.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why must a released migration never be edited?**

- A. Databases that already ran it would differ from new ones.
- B. Git does not allow it.
- C. SQLite caches migrations.
- D. It makes the list longer.

<details>
<summary>Answer</summary>

**A.** A changed step would only affect new databases, so old and new copies of the schema would silently disagree. Fix with a new step.

</details>

**Q2. Which change is safe while old code is still running?**

- A. Renaming `category` to `category_name`
- B. Adding a nullable `classifier_version` column
- C. Dropping the `reason` column
- D. Changing `confidence` from a number to text

<details>
<summary>Answer</summary>

**B.** Adding a nullable column is expand-only; old code never asks for it. The others break existing readers or writers.

</details>

**Q3. What does `migrate()` do on a database that is already up to date?**

- A. Re-runs every step
- B. Deletes the data
- C. Nothing, because `user_version` already equals the target
- D. Raises an error

<details>
<summary>Answer</summary>

**C.** It starts from the stored version, so running it again is safe: it is idempotent.

</details>

### Exercise 2 · Change: plan a rename the safe way (⏱️ ~20 min)

**Goal:** Rename a column without breaking anyone.

**Instructions:**
1. The team wants `evidence_excerpt` renamed to `evidence_sentence`.
2. Write the plan as three releases: expand (add the new column and fill it), switch (all code reads and writes the new one), contract (drop the old one).
3. Implement only the expand step as a new migration, with an `UPDATE` that copies existing values.
4. Write a test that an old reader using `evidence_excerpt` and a new reader using `evidence_sentence` both see the same data after the step.

<details>
<summary>Hint</summary>

SQLite's `ALTER TABLE` can add and drop columns; check the documentation for which version of SQLite you have before using `DROP COLUMN` in the contract step.

</details>

### Exercise 3 · Transfer: how does your team change schemas? (⏱️ ~10 min)

For a database you work with, find where its schema changes are recorded.
Check whether old code and new code ever run against it at the same time, and whether its recent changes were expand-only.

---

## 📖 Curated Resources

1. **[SQLite: ALTER TABLE](https://www.sqlite.org/lang_altertable.html)**
   - Why: what can change on a live table, and the restrictions.
2. **[SQLite: PRAGMA user_version](https://www.sqlite.org/pragma.html#pragma_user_version)**
   - Why: the version number this project's migrations rely on.
3. **[PostgreSQL: Modifying Tables](https://www.postgresql.org/docs/current/ddl-alter.html)**
   - Why: the same operations in PostgreSQL.
4. **[Python documentation: sqlite3 transaction control](https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions)**
   - Why: what `with connection:` does around each step.
5. **Book coverage for migrations:** none in the three books' freely available material; official documentation only.
   - Why: a book source should be chosen when the full books are available.
6. **Free source:** the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), Topic 27, "Don't Outrun Your Headlights".
   - Why: small, checkable steps, in the authors' own words.

---

## 🤔 Reflection Questions

1. **Comprehension:** What does "expand before contract" protect against?
2. **Application:** The weekly report uses `SELECT *` and checks the number of columns. What would you change first?
3. **Connection:** How is never editing a released migration like Day 11's rule of small, committed steps?
4. **Critical Thinking:** Is a migration that fills a new column for millions of rows still "safe"? What else would you measure?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 20: Protect invariants under concurrency](./day-20-invariants-under-concurrency.md). Two reviewers confirm the same company at once; you make sure only one wins.

**Before moving on, make sure you can:**

- [ ] Add a migration and explain why it is appended, not edited in.
- [ ] Explain `user_version` and what `migrate()` does with it.
- [ ] Test an old and a new reader against one upgraded database.

[← Previous: Day 18 Understand storage trade-offs](./day-18-storage-trade-offs.md) | [Course Home](../README.md) | [Next: Day 20 Protect invariants under concurrency →](./day-20-invariants-under-concurrency.md)
