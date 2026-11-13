"""Where About pages come from. The rest of the service only sees AboutPage."""
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Protocol

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


class WebsiteSource(Protocol):
    def about_page(self, company_name: str) -> AboutPage:
        """Return the company's About page or raise WebsiteUnavailable."""


class SampleWebsiteSource:
    """Reads the made-up sample companies. Used by tests and the tracer bullet."""

    def __init__(self, pages=SAMPLE_WEB):
        self._pages = pages

    def about_page(self, company_name):
        page = self._pages.get(company_name)
        if page is None:
            raise WebsiteUnavailable(company_name)
        return AboutPage(url=page["url"], text=page["about"])


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data.strip())


def fetch_with_urllib(url, timeout_seconds):
    with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
        return response.read().decode("utf-8", errors="replace")


class HttpWebsiteSource:
    """Reads real About pages over HTTP.

    The only class that knows about URLs, HTML and network timeouts.
    """

    def __init__(self, about_urls, fetch=fetch_with_urllib, timeout_seconds=5):
        self._about_urls = about_urls
        self._fetch = fetch
        self._timeout_seconds = timeout_seconds

    def about_page(self, company_name):
        url = self._about_urls.get(company_name)
        if url is None:
            raise WebsiteUnavailable(company_name)
        try:
            html = self._fetch(url, self._timeout_seconds)
        except OSError as error:
            raise WebsiteUnavailable(f"{company_name}: {error}") from error
        extractor = _TextExtractor()
        extractor.feed(html)
        text = " ".join(part for part in extractor.parts if part)
        if not text:
            raise WebsiteUnavailable(f"{company_name}: About page has no text")
        return AboutPage(url=url, text=text)
