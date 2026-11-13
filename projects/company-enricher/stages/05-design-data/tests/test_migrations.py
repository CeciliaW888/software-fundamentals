"""Day 19: old readers keep working while the schema grows."""
import sqlite3

from enricher.adapters.migrations import MIGRATIONS, migrate, schema_version

OLD_READER = "SELECT company_id, outcome, category FROM results"
NEW_READER = "SELECT company_id, coalesce(classifier_version, 'unknown') AS version FROM results"


def database_at_version_2_with_one_row():
    connection = sqlite3.connect(":memory:")
    migrate(connection, target=2)
    connection.execute("INSERT INTO companies VALUES ('c1', 'Saltwater Kitchen')")
    connection.execute(
        "INSERT INTO results (company_id, outcome, category, confidence, checked_at)"
        " VALUES ('c1', 'suggested', 'Food & Hospitality', 1.0, '2026-01-05T09:00:00+00:00')"
    )
    return connection


def test_migrate_upgrades_an_old_database_step_by_step():
    connection = database_at_version_2_with_one_row()
    migrate(connection)
    assert schema_version(connection) == len(MIGRATIONS)


def test_old_reader_still_works_after_the_new_column_is_added():
    connection = database_at_version_2_with_one_row()
    migrate(connection)
    assert connection.execute(OLD_READER).fetchall() == [("c1", "suggested", "Food & Hospitality")]


def test_new_reader_handles_rows_written_before_the_column_existed():
    connection = database_at_version_2_with_one_row()
    migrate(connection)
    assert connection.execute(NEW_READER).fetchall() == [("c1", "unknown")]


def test_running_migrate_twice_changes_nothing():
    connection = database_at_version_2_with_one_row()
    migrate(connection)
    migrate(connection)
    assert schema_version(connection) == len(MIGRATIONS)
