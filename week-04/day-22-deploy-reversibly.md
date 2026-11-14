# Day 22: Deploy reversibly

[← Previous: Day 21 Observe promises and failures](./day-21-observe-promises.md) | [Course Home](../README.md) | [Next: Day 23 Measure before optimizing →](./day-23-measure-before-optimizing.md)

> 📍 **Where we are in the story:** Week 4 · The service is almost ready for production. Now you run it, watch it, and recover when it fails.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:

1. Move settings out of code into the environment, with safe defaults and validation.
2. Ship new behaviour behind a feature flag that is off by default.
3. Run every stage's tests automatically on each push.
4. Plan the rollback for a change before you ship it.

**Plain idea:** every change you ship should have a quick, boring way to undo it.

**Difficulty:** 🔴 Advanced\
**Estimated Time:** 40 minutes (15 reading + 25 hands-on)\
**Module:** 6 · Operate what you build (lesson 0022)

---

## 📚 Core Concepts

### Observe: four ways a release can go wrong

Imagine the next release of the Company Enricher: it switches from the sample websites to real HTTP pages and lowers the threshold to 0.8.
List what could go wrong, and how long each would take to undo with the Module 5 code.

| Problem | Undo with the Module 5 code |
|---|---|
| Real websites time out | change code, review, release again |
| The new threshold sends wrong categories through | change a constant in code, release again |
| A bug in the new code | find the commit, revert, release again |
| A migration breaks the old version | restore the database from a backup |

Every undo is a code change or worse.
At 2 a.m., that is slow and risky.

### Say it plainly: make undo a switch, not a project

Stage 06 makes each of those undos faster.

**Settings from the environment.** `Settings.from_env` reads `ENRICHER_MIN_CONFIDENCE`, `ENRICHER_DB_PATH`, `ENRICHER_USE_HTTP_SOURCE`, and `ENRICHER_RETRY_ATTEMPTS`, with safe defaults.
Changing the threshold is restarting with a different value; undoing it is restarting with the old one.
Bad values, such as a threshold of 1.5, stop the service at startup with a clear message instead of running with nonsense.

**A feature flag.** `ENRICHER_USE_HTTP_SOURCE` is off by default.
`build_enricher` is the one place that reads it and wires either the sample source or the HTTP source.
The new code ships switched off, is switched on when ready, and is switched off again in seconds if it misbehaves.

**Expand-only migrations.** Day 19's rule means the previous version of the code still works on the new schema, so rolling back the code never needs rolling back the database.

**Automated tests on every push.** A GitHub Actions workflow runs `run_all_tests.sh`, every stage's tests, whenever the project changes.
A broken change is caught before it is merged, and `git revert` remains a one-command undo for anything that slips through.

Secrets, such as a future API key, follow the same path into settings but never into the repository.
OWASP's secrets guidance explains why and how.

### Name it: configuration, feature flags, reversibility

*The Pragmatic Programmer*, Topic 11, "Reversibility", argues that decisions are rarely final, so designs should make them easy to change.
Its Topic 32, "Configuration" recommends keeping values that may change after release, such as thresholds and service addresses, outside the code.

A **feature flag** is a setting that switches a piece of behaviour on or off without a code change.
A **rollback** returns a system to its previous working state.
**Continuous integration** runs the tests automatically on every change; GitHub Actions is one service that does this.

In the publisher's [official list of the book's tips](https://pragprog.com/tips/), Tip 18 (p. 48) is "There Are No Final Decisions", Tip 55 (p. 166) is "Parameterize Your App Using External Configuration", Tip 89 (p. 274) is "Use Version Control to Drive Builds, Tests, and Releases", and Tip 90 (p. 275) is "Test Early, Test Often, Test Automatically".
Topic 27, "Don't Outrun Your Headlights", available as the publisher's free excerpt on the [book page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), adds the habit underneath all of them: ship in small steps you can see the end of.

> **Key Insight:** Before shipping, write down the undo. If the undo is "write more code", make it a setting or a flag first.

---

## 🔑 Key Terminology

| Term | Definition | Source |
|------|-----------|--------|
| **Configuration** | Values that control a program's behaviour and can change without changing its code. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 32, "Configuration" |
| **Reversibility** | How easily a decision can be changed or undone later. | Paraphrased from Thomas and Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topic 11, "Reversibility" |
| **Environment variable** | A named value set outside a program that the program can read, such as `ENRICHER_DB_PATH`. | Official Python vocabulary ([os.environ](https://docs.python.org/3/library/os.html#os.environ)) |
| **Feature flag** | A setting that turns a piece of behaviour on or off without a code change. | Standard software vocabulary; this plain definition is course-authored |
| **Rollback** | Returning a system to its previous working state. | Standard software vocabulary; this plain definition is course-authored |
| **Continuous integration** | Running the tests automatically on every change. | Standard software vocabulary; see [GitHub Actions documentation](https://docs.github.com/en/actions) |

---

## 💻 Code Examples

### Example 1: Settings with defaults and validation

*File: [`projects/company-enricher/stages/06-operate/enricher/settings.py`](../projects/company-enricher/stages/06-operate/enricher/settings.py)*

```python
@classmethod
def from_env(cls, environ=None):
    environ = os.environ if environ is None else environ
    defaults = cls()
    settings = cls(
        minimum_confidence=float(environ.get("ENRICHER_MIN_CONFIDENCE", defaults.minimum_confidence)),
        database_path=environ.get("ENRICHER_DB_PATH", defaults.database_path),
        use_http_source=environ.get("ENRICHER_USE_HTTP_SOURCE", "false").lower() == "true",
        retry_attempts=int(environ.get("ENRICHER_RETRY_ATTEMPTS", defaults.retry_attempts)),
    )
    if not 0.0 < settings.minimum_confidence <= 1.0:
        raise ValueError("ENRICHER_MIN_CONFIDENCE must be above 0 and at most 1")
    if settings.retry_attempts < 1:
        raise ValueError("ENRICHER_RETRY_ATTEMPTS must be at least 1")
    return settings
```

**What's happening:** `environ` can be passed in, so tests check settings without touching the real environment.

### Example 2: One place reads the flag

*File: [`projects/company-enricher/stages/06-operate/enricher/app.py`](../projects/company-enricher/stages/06-operate/enricher/app.py)*

```python
if settings.use_http_source:
    source = HttpWebsiteSource(about_urls or {})
else:
    source = SampleWebsiteSource()
```

**What's happening:** the rest of the service never knows which source it got, thanks to Day 10's boundary.

### Example 3: Tests on every push

*File: [`.github/workflows/company-enricher-tests.yml`](../.github/workflows/company-enricher-tests.yml)*

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest
      - run: ./projects/company-enricher/run_all_tests.sh
```

### Example 4: The rollback plan, written down

```bash
# Real websites misbehave: switch the flag off and restart.
ENRICHER_USE_HTTP_SOURCE=false python -m enricher
# The threshold change was wrong: restart with the old value.
ENRICHER_MIN_CONFIDENCE=0.82 python -m enricher
# A code change was wrong: undo that commit; the schema still works for old code.
git revert --no-edit <commit>
```

---

## ✏️ Hands-On Exercises

### Exercise 1 · Check (⏱️ ~3 min)

**Q1. Why is `ENRICHER_USE_HTTP_SOURCE` off by default?**

- A. HTTP is slower.
- B. New behaviour ships switched off and is turned on deliberately, so turning it off is the rollback.
- C. Python cannot read true.
- D. The sample source is more accurate.

<details>
<summary>Answer</summary>

**B.** A flag that defaults to the old behaviour makes the safe state the default, and undo a setting change.

</details>

**Q2. Why does `from_env` refuse a threshold of 1.5 at startup?**

- A. Because floats cannot exceed 1
- B. To save memory
- C. To crash early on a configuration mistake instead of running with nonsense
- D. Because the tests require it

<details>
<summary>Answer</summary>

**C.** A bad setting caught at startup is a clear, immediate failure, like Day 8's impossible confidence.

</details>

**Q3. Why can the code be rolled back without rolling back the database?**

- A. SQLite has no schema.
- B. Rollbacks delete the database.
- C. The flag controls the schema.
- D. Migrations are expand-only, so older code still works with the newer schema.

<details>
<summary>Answer</summary>

**D.** Day 19's expand-before-contract rule is what makes code rollback safe.

</details>

### Exercise 2 · Change: flag a new behaviour (⏱️ ~20 min)

**Goal:** Ship a change that can be switched off.

**Instructions:**
1. New behaviour: when the partner directory hint and the website agree, accept at a lower threshold of 0.6.
2. Add a flag `ENRICHER_TRUST_AGREEING_SOURCES`, default off, to `Settings`.
3. Pass it into `SuggestionPolicy` from `build_enricher`, and implement the rule only when the flag is on.
4. Write tests for flag off (old behaviour unchanged) and flag on, then run `./run_all_tests.sh` from `projects/company-enricher`.

<details>
<summary>Hint</summary>

Keep the existing policy tests unchanged: if any of them fails with the flag off, the default behaviour changed.

</details>

### Exercise 3 · Transfer: write the undo (⏱️ ~10 min)

For the last change you shipped or reviewed, write its rollback in three lines.
If any line says "write code", decide which setting or flag would have shortened it.

---

## 📖 Curated Resources

1. **Practice reading:** David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary Edition, Topics 11, "Reversibility" and 32, "Configuration".
   - 🔗 [Publisher page](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
   - Why: keeping decisions changeable and values outside the code.
2. **[GitHub Actions documentation](https://docs.github.com/en/actions)**
   - Why: how the workflow in Example 3 runs.
3. **[Git documentation: git-revert](https://git-scm.com/docs/git-revert)**
   - Why: undoing a released commit.
4. **[OWASP: Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)**
   - Why: how secrets differ from ordinary settings.
5. **[Python documentation: os.environ](https://docs.python.org/3/library/os.html#os.environ)**
   - Why: how environment variables reach the program.

---

## 🤔 Reflection Questions

1. **Comprehension:** What makes a rollback "boring", and why is that good?
2. **Application:** Which of the service's settings would you never let change without a code review?
3. **Connection:** Which earlier lessons made today's rollbacks possible?
4. **Critical Thinking:** Can too many flags become a source of complexity? How would you retire one?

Stop and ask whenever a word feels harder than the idea.

---

## ➡️ Next Steps

**Tomorrow:** [Day 23: Measure before optimizing](./day-23-measure-before-optimizing.md). The batch is getting slower; you will find out why before changing anything.

**Before moving on, make sure you can:**

- [ ] Read settings from the environment with defaults and validation.
- [ ] Ship behaviour behind a flag that defaults to off.
- [ ] Write the rollback for a change before shipping it.

[← Previous: Day 21 Observe promises and failures](./day-21-observe-promises.md) | [Course Home](../README.md) | [Next: Day 23 Measure before optimizing →](./day-23-measure-before-optimizing.md)
