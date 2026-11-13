"""The words the business uses, as code.

Value objects (Confidence, Evidence, CategorySuggestion) are equal when
their values are equal and never change. Company is an entity: it keeps
its identity even if its name changes.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from enricher.core.categories import Category


@dataclass(frozen=True)
class Confidence:
    value: float

    def __post_init__(self):
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"confidence must be between 0 and 1, got {self.value!r}")

    def at_least(self, minimum):
        return self.value >= minimum


@dataclass(frozen=True)
class Evidence:
    source_url: str
    excerpt: str


@dataclass(frozen=True)
class CategorySuggestion:
    category: Category
    confidence: Confidence


@dataclass(eq=False)
class Company:
    company_id: str
    name: str
    directory_hint: Category | None = field(default=None)

    def __eq__(self, other):
        return isinstance(other, Company) and other.company_id == self.company_id

    def __hash__(self):
        return hash(self.company_id)


class Outcome(Enum):
    SUGGESTED = "suggested"
    NEEDS_REVIEW = "needs_review"


class ReviewReason(Enum):
    WEAK_EVIDENCE = "weak_evidence"
    NO_WEBSITE = "no_website"
    CONFLICTING_SOURCES = "conflicting_sources"


@dataclass(frozen=True)
class EnrichmentResult:
    company: Company
    outcome: Outcome
    reason: ReviewReason | None
    suggestion: CategorySuggestion | None
    evidence: Evidence | None
    checked_at: datetime
