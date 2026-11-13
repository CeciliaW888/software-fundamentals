"""The Company Enricher after Module 1.

Same decisions as the inherited script, with names that explain the job
and a stated promise for the main function.
"""
import re
from dataclasses import dataclass

from sample_web import SAMPLE_WEB

CATEGORIES = [
    "Retail",
    "Wholesale & Distribution",
    "Manufacturing",
    "Software & IT",
    "Healthcare",
    "Food & Hospitality",
    "Construction",
    "Finance",
    "Education",
    "Other",
]

CATEGORY_KEYWORDS = {
    "Retail": {"store", "shop", "sells", "retail", "boutique"},
    "Wholesale & Distribution": {"wholesale", "distribute", "distribution", "bulk", "warehouse"},
    "Manufacturing": {"manufacture", "manufacturing", "factory", "fabricate", "bake"},
    "Software & IT": {"software", "cloud", "technology", "apps", "hosting"},
    "Healthcare": {"clinic", "patients", "dental", "medical", "health"},
    "Food & Hospitality": {"restaurant", "cafe", "cafes", "catering", "breakfast", "lunch", "dinner", "bread", "pastries"},
    "Construction": {"build", "homes", "renovate", "construction", "builders"},
    "Finance": {"loans", "lending", "insurance", "banking", "accounting"},
    "Education": {"teach", "courses", "students", "exam", "school"},
    "Other": set(),
}


@dataclass(frozen=True)
class CategorySuggestion:
    category: str
    confidence: float


class WebsiteUnavailable(Exception):
    """No suitable official website or About page could be read."""


class KeywordCategoryClassifier:
    """Suggests a category by counting category keywords in a text."""

    def predict_proba(self, about_page_texts):
        """Return one list of probabilities per text, in CATEGORIES order."""
        probabilities_by_text = []
        for text in about_page_texts:
            words = re.findall(r"[a-z]+", text.lower())
            hits = [sum(1 for word in words if word in CATEGORY_KEYWORDS[category]) for category in CATEGORIES]
            total_hits = sum(hits)
            if total_hits == 0:
                probabilities_by_text.append([1 / len(CATEGORIES)] * len(CATEGORIES))
            else:
                probabilities_by_text.append([count / total_hits for count in hits])
        return probabilities_by_text

    def suggest(self, activity_summary):
        """Return the most likely category and its confidence."""
        probabilities = self.predict_proba([activity_summary])[0]
        confidence = max(probabilities)
        if confidence == 1 / len(CATEGORIES):
            return CategorySuggestion("Other", confidence)
        return CategorySuggestion(CATEGORIES[probabilities.index(confidence)], confidence)


def select_confident_category_suggestions(
    about_page_texts,
    category_classifier,
    minimum_confidence=0.82,
):
    probabilities_by_page = (
        category_classifier.predict_proba(
            about_page_texts
        )
    )
    return [
        about_text
        for about_text, probabilities
        in zip(
            about_page_texts,
            probabilities_by_page,
        )
        if max(probabilities)
        >= minimum_confidence
    ]


def find_official_website(company_name):
    """Return the company's website address, or raise WebsiteUnavailable."""
    page = SAMPLE_WEB.get(company_name)
    if page is None:
        raise WebsiteUnavailable(company_name)
    return page["url"]


def read_about_page(website):
    """Return the About-page text published at a website address."""
    for page in SAMPLE_WEB.values():
        if page["url"] == website:
            return page["about"]
    raise WebsiteUnavailable(website)


def summarise_business_activity(about_text):
    """Return the first sentence, which usually states the main activity."""
    return about_text.split(".")[0]


class SuggestionList:
    """Keeps accepted suggestions in memory, in the order they were saved."""

    def __init__(self):
        self.saved_suggestions = []

    def save(self, company_name, suggestion):
        self.saved_suggestions.append((company_name, suggestion))


def suggest_company_category(
    company_name,
    classifier,
    store,
):
    """Suggest a business category for one company.

    Reads the company's official website
    and About page.
    Returns the saved suggestion when its
    confidence is at least 0.82.
    Returns None when evidence is weaker.
    Saves an accepted suggestion to store.
    Raises WebsiteUnavailable when no
    suitable page can be read.
    """
    website = find_official_website(
        company_name
    )
    about_text = read_about_page(website)
    activity_summary = (
        summarise_business_activity(
            about_text
        )
    )
    suggestion = classifier.suggest(
        activity_summary
    )

    if suggestion.confidence < 0.82:
        return None

    store.save(company_name, suggestion)
    return suggestion


if __name__ == "__main__":
    store = SuggestionList()
    for company_name in SAMPLE_WEB:
        print(company_name, suggest_company_category(company_name, KeywordCategoryClassifier(), store))
