"""Schema versions, applied in order. Never edit a released step; add a new one.

SQLite keeps the current version number in PRAGMA user_version.
"""

MIGRATIONS = [
    # 1: tables shaped by the access patterns (Day 17)
    """
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
    """,
    # 2: an index for the review queue (Day 18)
    """
    CREATE INDEX results_review_queue
        ON results (outcome, checked_at);
    """,
    # 3: expand only: a new nullable column old readers can ignore (Day 19)
    """
    ALTER TABLE results ADD COLUMN classifier_version TEXT;
    """,
    # 4: at most one confirmed category per company (Day 20)
    """
    CREATE TABLE confirmations (
        company_id   TEXT NOT NULL REFERENCES companies (company_id),
        category     TEXT NOT NULL,
        confirmed_by TEXT NOT NULL,
        confirmed_at TEXT NOT NULL
    );
    CREATE UNIQUE INDEX one_confirmation_per_company
        ON confirmations (company_id);
    """,
]


def schema_version(connection):
    return connection.execute("PRAGMA user_version").fetchone()[0]


def migrate(connection, target=len(MIGRATIONS)):
    """Apply every step between the database's version and target."""
    current = schema_version(connection)
    for version in range(current + 1, target + 1):
        with connection:
            connection.executescript(MIGRATIONS[version - 1])
            connection.execute(f"PRAGMA user_version = {version}")
