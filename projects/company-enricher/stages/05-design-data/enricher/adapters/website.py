"""Website sources: sample data for tests, HTTP for real pages."""
import urllib.request
from html.parser import HTMLParser

from enricher.adapters.sample_web import SAMPLE_WEB
from enricher.core.ports import AboutPage, WebsiteUnavailable


class SampleWebsiteSource:
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
