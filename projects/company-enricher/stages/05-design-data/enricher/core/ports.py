"""What the core needs from the outside world, in the core's own words."""
from dataclasses import dataclass
from typing import Protocol


class WebsiteUnavailable(Exception):
    """No suitable official website or About page could be read."""


@dataclass(frozen=True)
class AboutPage:
    url: str
    text: str

    @property
    def main_activity(self):
        """The first sentence, which usually states what the business does."""
        return self.text.split(".")[0]


class WebsiteSource(Protocol):
    def about_page(self, company_name: str) -> AboutPage:
        """Return the company's About page or raise WebsiteUnavailable."""


class ResultStore(Protocol):
    def save(self, result) -> None:
        """Record one enrichment result, whatever its outcome."""
