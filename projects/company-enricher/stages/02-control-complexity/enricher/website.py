"""Find a company's About page. Callers never see URLs or page lookups."""
from dataclasses import dataclass

from enricher.sample_web import SAMPLE_WEB


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


class CompanyWebsites:
    """One call answers "what does this company say about itself?"."""

    def __init__(self, pages=SAMPLE_WEB):
        self._pages = pages

    def about_page(self, company_name):
        page = self._pages.get(company_name)
        if page is None:
            raise WebsiteUnavailable(company_name)
        return AboutPage(url=page["url"], text=page["about"])
