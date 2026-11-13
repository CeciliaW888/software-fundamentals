"""Results and confirmations in SQLite, shaped by how reviewers use them."""
import sqlite3
from datetime import datetime

from enricher.adapters.migrations import migrate
from enricher.core.categories import Category
from enricher.core.model import Outcome

CLASSIFIER_VERSION = "keywords-1"


def idempotency_key(result):
    """Same run and same company means the same result: record it once."""
    if result.run_id is None:
        return None
    return f"{result.run_id}:{result.company.company_id}"


class AlreadyConfirmed(Exception):
    """Another reviewer has already confirmed a category for this company."""


class SqliteResultStore:
    def __init__(self, path=":memory:"):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        migrate(self.connection)

    def save(self, result):
        """Access pattern 1: record every enrichment result."""
        suggestion, evidence = result.suggestion, result.evidence
        with self.connection:
            self.connection.execute(
                "INSERT INTO companies (company_id, name) VALUES (?, ?)"
                " ON CONFLICT (company_id) DO UPDATE SET name = excluded.name",
                (result.company.company_id, result.company.name),
            )
            self.connection.execute(
                """INSERT INTO results (company_id, outcome, reason, category, confidence,
                                        evidence_url, evidence_excerpt, checked_at, classifier_version,
                                        idempotency_key)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT (idempotency_key) DO NOTHING""",
                (
                    result.company.company_id,
                    result.outcome.value,
                    result.reason.value if result.reason else None,
                    suggestion.category.value if suggestion else None,
                    suggestion.confidence.value if suggestion else None,
                    evidence.source_url if evidence else None,
                    evidence.excerpt if evidence else None,
                    result.checked_at.isoformat(),
                    CLASSIFIER_VERSION,
                    idempotency_key(result),
                ),
            )

    def latest_result(self, company_id):
        """Access pattern 2: the newest result for one company."""
        return self.connection.execute(
            "SELECT * FROM results WHERE company_id = ? ORDER BY checked_at DESC, result_id DESC LIMIT 1",
            (company_id,),
        ).fetchone()

    def review_queue(self, limit=20):
        """Access pattern 3: results waiting for a person, oldest first."""
        return self.connection.execute(
            "SELECT * FROM results WHERE outcome = ? ORDER BY checked_at LIMIT ?",
            (Outcome.NEEDS_REVIEW.value, limit),
        ).fetchall()

    def history(self, company_id):
        """Access pattern 4: every result for one company, oldest first."""
        return self.connection.execute(
            "SELECT * FROM results WHERE company_id = ? ORDER BY checked_at, result_id",
            (company_id,),
        ).fetchall()

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
