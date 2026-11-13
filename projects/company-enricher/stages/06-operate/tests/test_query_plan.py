"""Day 18: the review-queue query must use the index, not scan the table."""
from enricher.adapters.migrations import MIGRATIONS, migrate
import sqlite3

QUEUE_QUERY = "SELECT * FROM results WHERE outcome = ? ORDER BY checked_at LIMIT ?"


def plan(connection):
    rows = connection.execute("EXPLAIN QUERY PLAN " + QUEUE_QUERY, ("needs_review", 20)).fetchall()
    return " | ".join(row[-1] for row in rows)


def test_without_the_index_the_queue_query_scans_every_row():
    connection = sqlite3.connect(":memory:")
    migrate(connection, target=1)
    assert "SCAN results" in plan(connection)


def test_with_the_index_the_queue_query_searches_it():
    connection = sqlite3.connect(":memory:")
    migrate(connection, target=len(MIGRATIONS))
    assert "SEARCH results USING INDEX results_review_queue (outcome=?)" in plan(connection)
