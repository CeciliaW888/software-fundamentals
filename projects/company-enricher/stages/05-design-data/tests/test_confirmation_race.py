"""Day 20: reproduce the check-then-insert anomaly, then show the fix."""
import sqlite3
import sys
from pathlib import Path

import pytest

from enricher.adapters.migrations import migrate

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from day20_check_then_insert import insert_confirmation, no_confirmation_yet  # noqa: E402


def shared_database(tmp_path, with_unique_index):
    path = tmp_path / "enricher.db"
    setup = sqlite3.connect(path)
    migrate(setup, target=3)
    setup.execute("INSERT INTO companies VALUES ('c1', 'Lantern Lane Bakery')")
    setup.executescript(
        """CREATE TABLE confirmations (company_id TEXT NOT NULL, category TEXT NOT NULL,
                                       confirmed_by TEXT NOT NULL, confirmed_at TEXT NOT NULL);"""
        + ("CREATE UNIQUE INDEX one_confirmation_per_company ON confirmations (company_id);" if with_unique_index else "")
    )
    setup.commit()
    return sqlite3.connect(path), sqlite3.connect(path)


def test_two_reviewers_can_both_confirm_without_a_constraint(tmp_path):
    reviewer_a, reviewer_b = shared_database(tmp_path, with_unique_index=False)

    a_sees_none = no_confirmation_yet(reviewer_a, "c1")
    b_sees_none = no_confirmation_yet(reviewer_b, "c1")
    insert_confirmation(reviewer_a, "c1", "Food & Hospitality", "a", "t1")
    insert_confirmation(reviewer_b, "c1", "Manufacturing", "b", "t2")

    assert a_sees_none and b_sees_none
    assert reviewer_a.execute("SELECT count(*) FROM confirmations").fetchone()[0] == 2  # the invariant is broken


def test_the_unique_index_makes_the_second_confirmation_fail(tmp_path):
    reviewer_a, reviewer_b = shared_database(tmp_path, with_unique_index=True)

    assert no_confirmation_yet(reviewer_a, "c1") and no_confirmation_yet(reviewer_b, "c1")
    insert_confirmation(reviewer_a, "c1", "Food & Hospitality", "a", "t1")

    with pytest.raises(sqlite3.IntegrityError):
        insert_confirmation(reviewer_b, "c1", "Manufacturing", "b", "t2")
