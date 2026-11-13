"""The HTTP adapter is tested with a fake fetch: no network in tests."""
import pytest

from enricher.website import HttpWebsiteSource, WebsiteUnavailable

URLS = {"Saltwater Kitchen": "https://saltwaterkitchen.example/about"}


def test_extracts_text_from_html():
    def fetch(url, timeout_seconds):
        return "<html><body><h1>About</h1><p>A seaside restaurant and cafe.</p></body></html>"

    page = HttpWebsiteSource(URLS, fetch=fetch).about_page("Saltwater Kitchen")

    assert page.url == "https://saltwaterkitchen.example/about"
    assert "seaside restaurant" in page.text


def test_network_error_becomes_website_unavailable():
    def fetch(url, timeout_seconds):
        raise TimeoutError("timed out")

    with pytest.raises(WebsiteUnavailable):
        HttpWebsiteSource(URLS, fetch=fetch).about_page("Saltwater Kitchen")


def test_passes_its_timeout_to_fetch():
    seen = {}

    def fetch(url, timeout_seconds):
        seen["timeout"] = timeout_seconds
        return "<p>Restaurant.</p>"

    HttpWebsiteSource(URLS, fetch=fetch, timeout_seconds=3).about_page("Saltwater Kitchen")
    assert seen["timeout"] == 3
