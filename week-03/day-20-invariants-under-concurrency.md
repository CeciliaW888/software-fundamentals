# Day 20: Protect invariants under concurrency

[← Previous: Day 19 Evolve schemas without coordinated deployment](./day-19-evolve-schemas.md) | [Course Home](../README.md) | [Next: Day 21 Observe promises and failures →](../week-04/day-21-observe-promises.md)

> 📍 **Where we are in the story:** Week 3 · The model fits the business. Now the data it keeps has to evolve without breaking.

---

> **Book coverage:** *The Pragmatic Programmer*'s Topic 34 and Evans's *Domain-Driven Design*, Chapter 6 (aggregates), cover the race and the consistency boundary.
> Database isolation levels are not covered in the three books, so that part relies on the official SQLite and PostgreSQL documentation.

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. State a business invariant precisely.
2. Reproduce a check-then-act race with two database connections.
3. Explain why checking in application code cannot protect an invariant on its own.
4. Let the database enforce the invariant with a unique index, and turn the violation into a domain error.

**Plain idea:** when two people can act at the same time, a rule must be enforced where both actions meet, not where each one checks.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 45 minutes (20 reading + 25 hands-on)\
**Module:** 5 · Design data that can evolve (lesson 0020)

---

## 📚 Core Concepts

### Observe: two reviewers, one bakery

Lantern Lane Bakery is in the review queue.
Two reviewers open it at almost the same moment.
Reviewer A decides Food & Hospitality; reviewer B decides Manufacturing.

The obvious code for "confirm a category" is: check whether a confirmation already exists; if not, insert one.
The exercise file `day20_check_then_insert.py` does exactly that.
The test `test_two_reviewers_can_both_confirm_without_a_constraint` runs the steps in this order, with two separate database connections:

1. A checks: no confirmation yet.
2. B checks: no confirmation yet.
3. A inserts Food & Hospitality.
4. B inserts Manufacturing.

Both inserts succeed.
The bakery now has two confirmed categories, and every report that assumes one will be wrong.
Nothing crashed; the data is simply inconsistent.

### Say it plainly: the check and the act must be one step

The rule is: **a company has at most one confirmed category**.
A rule that must always be true is an invariant.

Each reviewer's check was correct when it ran.
The problem is the gap between the check and the insert, during which the other reviewer acted.
Any rule enforced by "look first, then write" has that gap, however fast the code is.

The fix is to let the place where both writes meet, the database, refuse the second one.
Migration 4 adds a unique index on `confirmations (company_id)`.
Now step 4 fails with an `IntegrityError`, whatever order the steps run in.
`SqliteResultStore.confirm_category` turns that error into a domain exception, `AlreadyConfirmed`, so the reviewer screen can say "someone else confirmed this first" instead of showing a database error.

### Name it: invariants, aggregates, isolation

An **invariant** is a rule that must always hold.
A **race condition** is a bug where the result depends on the timing of concurrent actions; check-then-act is the classic shape.

Eric Evans's *Domain-Driven Design*, Chapter 6, "The Life Cycle of a Domain Object", introduces the **aggregate**: a cluster of objects treated as one unit for data changes, with a boundary inside which invariants must always be consistent.
Here, a company together with its confirmation is that unit, and the database constraint is how the boundary is enforced.

*The Pragmatic Programmer*, Topic 34, "Shared State Is Incorrect State", warns that whenever two processes share a resource, you must make access to it atomic, or race conditions follow.

Databases describe how concurrent transactions see each other as **isolation**.
SQLite's documentation explains its isolation behaviour, including that only one connection can write at a time; PostgreSQL's documentation describes its isolation levels and the anomalies each allows.
Neither makes a check-then-act sequence safe on its own: in this example each check runs before either write, so a constraint is the dependable guard.

*The Pragmatic Programmer*'s Topic 34, "Shared State Is Incorrect State", available as the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), tells the same story with a diner, two waiters, and the last slice of pie: each waiter checks the display case and promises the slice, because the check and the taking are not one indivisible step.
The book's remedies are mutual exclusion and, better, making the shared resource itself responsible for its own consistency, so callers cannot forget to protect it.
The unique index is that second remedy: the database, not each reviewer's code, guards the rule.
Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) explains why the rule needs one owner: an aggregate draws a boundary around objects whose consistency rules must hold together, and changes inside it are applied as one unit.
Chapter 6 makes the point with a purchase order edited by two people at once: each change is valid alone, yet together they break a rule about the whole order, which is why the rule must be checked for the order as one unit.

> **Key Insight:** Enforce an invariant at the single point every writer must pass through. For stored data, that is usually a database constraint.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Invariant** | A rule that must always be true, such as "a company has at most one confirmed category". | Standard software vocabulary; this plain definition is course-authored |
| **Race condition** | A bug where the outcome depends on the timing of actions that happen at the same time. | Standard software vocabulary; this plain definition is course-authored |
| **Aggregate** | A cluster of objects treated as one unit for changes, with a boundary inside which invariants must hold. | Paraphrased from Eric Evans, *Domain-Driven Design*, Chapter 6 |
| **Unique index** | An index that refuses two rows with the same value in its columns. | Official SQLite vocabulary ([CREATE INDEX](https://www.sqlite.org/lang_createindex.html)) |
| **Transaction** | A group of database changes that succeed or fail together. | Official SQLite vocabulary ([transactions](https://www.sqlite.org/lang_transaction.html)) |
| **Isolation** | How much one transaction can see of another's changes while both are running. | Official SQLite vocabulary ([isolation in SQLite](https://www.sqlite.org/isolation.html)) |

---

## 💻 Code Examples

### Example 1: The unsafe pattern

*File: [`projects/company-enricher/stages/05-design-data/exercises/day20_check_then_insert.py`](../projects/company-enricher/stages/05-design-data/exercises/day20_check_then_insert.py)*

```python
def no_confirmation_yet(connection, company_id):
    row = connection.execute(
        "SELECT 1 FROM confirmations WHERE company_id = ?", (company_id,)
    ).fetchone()
    return row is None
```

**What's happening:** the answer is true when it is read, and may be false a moment later.

### Example 2: Reproducing the race

*File: [`projects/company-enricher/stages/05-design-data/tests/test_confirmation_race.py`](../projects/company-enricher/stages/05-design-data/tests/test_confirmation_race.py)*

```python
def test_two_reviewers_can_both_confirm_without_a_constraint(tmp_path):
    reviewer_a, reviewer_b = shared_database(tmp_path, with_unique_index=False)

    a_sees_none = no_confirmation_yet(reviewer_a, "c1")
    b_sees_none = no_confirmation_yet(reviewer_b, "c1")
    insert_confirmation(reviewer_a, "c1", "Food & Hospitality", "a", "t1")
    insert_confirmation(reviewer_b, "c1", "Manufacturing", "b", "t2")

    assert a_sees_none and b_sees_none
    assert reviewer_a.execute("SELECT count(*) FROM confirmations").fetchone()[0] == 2  # the invariant is broken
```

**What's happening:** the test runs the steps in the bad order on purpose, so the race happens every time instead of once a month in production.

### Example 3: The database enforces the rule

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/migrations.py)*

```sql
CREATE UNIQUE INDEX one_confirmation_per_company
    ON confirmations (company_id);
```

### Example 4: A database error becomes a domain answer

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/sqlite_store.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/sqlite_store.py)*

```python
def confirm_category(self, company_id, category: Category, reviewer, at: datetime):
    """Record a reviewer's confirmed category. Only the first one wins."""
    try:
        with self.connection:
            self.connection.execute(
                "INSERT INTO confirmations (company_id, category, confirmed_by, confirmed_at)"
                " VALUES (?, ?, ?, ?)",
                (company_id, category.value, reviewer, at.isoformat()),
            )
    except sqlite3.IntegrityError as error:
        raise AlreadyConfirmed(company_id) from error
```

**What's happening:** no check before the insert at all; the insert either wins or is refused, in one step.

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why does "check, then insert" fail with two reviewers?**

- A. The check is written in SQL.
- B. SQLite cannot run two queries.
- C. The reviewers use different categories.
- D. Another write can happen between the check and the insert.

<details>
<summary>Answer</summary>

**D.** The gap between check and act is where the other reviewer's write lands. Speed does not remove the gap.

</details>

**Q2. Where should the "one confirmation per company" rule be enforced?**

- A. In the database, where every write must pass
- B. In the reviewer screen's JavaScript
- C. In a comment in the code
- D. In each reviewer's head

<details>
<summary>Answer</summary>

**A.** The database is the single point every writer goes through, so a constraint there holds regardless of timing.

</details>

**Q3. Why does `confirm_category` raise `AlreadyConfirmed` instead of letting `IntegrityError` through?**

- A. To hide a bug
- B. So callers deal with a business situation in business words
- C. Because `IntegrityError` cannot be caught
- D. To retry automatically

<details>
<summary>Answer</summary>

**B.** The core and the reviewer screen should not need to know SQLite's exception types; the adapter translates, as on Day 10.

</details>

### Exercise 2 · Change: a reviewer changes their mind (⏱️ ~20 min)

**Goal:** Change an invariant-protected value safely.

**Instructions:**
1. Reviewers may correct a confirmation, but only the reviewer who made it.
2. Add `change_confirmation(company_id, category, reviewer, at)` to `SqliteResultStore` using one `UPDATE ... WHERE company_id = ? AND confirmed_by = ?`.
3. Check the number of changed rows (`cursor.rowcount`) and raise a domain error when it is zero.
4. Write two tests: the original reviewer can change it; another reviewer cannot.

<details>
<summary>Hint</summary>

Putting the reviewer condition inside the `WHERE` makes the check and the change one statement, so there is no gap.

</details>

### Exercise 3 · Transfer: find a check-then-act (⏱️ ~10 min)

Search a codebase you know for a pattern like "if not exists, then create" or "if balance enough, then subtract".
Decide whether two users could hit it at once, and what would enforce the rule in one step.

---

## 🔁 Module 5 · Before / After

**Before:** after Module 4 the model spoke the business's language, but results lived in a Python list: only suggested results were kept, everything vanished on restart, and reviewers had no queue.

*File: [`projects/company-enricher/stages/04-model-the-domain/enricher/adapters/store.py`](../projects/company-enricher/stages/04-model-the-domain/enricher/adapters/store.py)*

```python
class InMemoryResultStore:
    def __init__(self):
        self.saved_results = []

    def save(self, result):
        self.saved_results.append(result)
```

**After:** quality has measurable targets checked by a test, every result is stored in SQLite in tables shaped by four access patterns, the review queue uses an index whose plan is pinned by a test, the schema evolves through numbered expand-only migrations, and the one-confirmation rule is enforced by the database.

*File: [`projects/company-enricher/stages/05-design-data/enricher/adapters/sqlite_store.py`](../projects/company-enricher/stages/05-design-data/enricher/adapters/sqlite_store.py)*

```python
def review_queue(self, limit=20):
    """Access pattern 3: results waiting for a person, oldest first."""
    return self.connection.execute(
        "SELECT * FROM results WHERE outcome = ? ORDER BY checked_at LIMIT ?",
        (Outcome.NEEDS_REVIEW.value, limit),
    ).fetchall()
```

---

## 📖 Curated Resources

1. **Domain reading:** Eric Evans, *Domain-Driven Design*, Chapter 6, "The Life Cycle of a Domain Object".
   - 🔗 [DDD resources from Domain Language](https://www.domainlanguage.com/ddd/)
   - Why: aggregates as consistency boundaries for invariants.
2. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 34, "Shared State Is Incorrect State".
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: why shared resources need atomic access.
3. **[SQLite: Isolation In SQLite](https://www.sqlite.org/isolation.html)** and **[Transactions](https://www.sqlite.org/lang_transaction.html)**
   - Why: what SQLite guarantees when several connections use one database.
4. **[PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)**
   - Why: isolation levels and the anomalies each one allows.
5. **Book coverage for isolation levels:** none in the three books; official documentation only.
6. **Free sources:** the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) (Topic 34) and Evans's free [*DDD Reference*](https://www.domainlanguage.com/ddd/reference/) (aggregates).
   - Why: the race and its remedies, and the consistency boundary, in the authors' own words.

---

## 🤔 Reflection Questions

1. **Comprehension:** What exactly happens in the gap between a check and an act?
2. **Application:** Which other invariant in the Company Enricher could two concurrent batch runs break?
3. **Connection:** How is the unique index like Day 13's `Confidence` value object?
4. **Critical Thinking:** Can every invariant be written as a database constraint? What would you do for one that can't?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 21: Observe promises and failures](../week-04/day-21-observe-promises.md). Module 6 begins: the service is almost ready for production, so now you run it, watch it, and recover when it fails.

**Before moving on, make sure you can:**

- [ ] State the confirmation invariant precisely.
- [ ] Explain and reproduce the check-then-act race.
- [ ] Enforce an invariant with a constraint and translate its error.

[← Previous: Day 19 Evolve schemas without coordinated deployment](./day-19-evolve-schemas.md) | [Course Home](../README.md) | [Next: Day 21 Observe promises and failures →](../week-04/day-21-observe-promises.md)
