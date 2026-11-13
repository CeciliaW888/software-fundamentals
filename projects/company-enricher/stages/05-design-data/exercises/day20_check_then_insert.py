"""Day 20 exercise: the unsafe way to confirm a category.

Each reviewer checks for an existing confirmation, then inserts one.
Two reviewers who both check before either inserts both "win".
"""


def no_confirmation_yet(connection, company_id):
    row = connection.execute(
        "SELECT 1 FROM confirmations WHERE company_id = ?", (company_id,)
    ).fetchone()
    return row is None


def insert_confirmation(connection, company_id, category, reviewer, at):
    with connection:
        connection.execute(
            "INSERT INTO confirmations (company_id, category, confirmed_by, confirmed_at)"
            " VALUES (?, ?, ?, ?)",
            (company_id, category, reviewer, at),
        )
