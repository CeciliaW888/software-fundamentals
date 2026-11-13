"""Configuration from environment variables, with safe defaults (Day 22).

Changing a setting needs a restart, not a code change, so a bad value can
be rolled back by restoring the previous environment.
"""
import os
from dataclasses import dataclass

from enricher.core.policy import MINIMUM_CONFIDENCE


@dataclass(frozen=True)
class Settings:
    minimum_confidence: float = MINIMUM_CONFIDENCE
    database_path: str = "enricher.db"
    use_http_source: bool = False  # feature flag: off until the HTTP source is proven
    retry_attempts: int = 3

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
