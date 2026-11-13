"""Anticorruption layer for the Tradeline Directory, a made-up partner feed.

The partner has its own model: listing IDs, legal trading names and
three-letter sector codes. This adapter translates a listing into our
Company, so none of the partner's words reach the core.
"""
from enricher.core.categories import Category
from enricher.core.model import Company

SECTOR_CODE_TO_CATEGORY = {
    "RTL": Category.RETAIL,
    "WHS": Category.WHOLESALE,
    "MFG": Category.MANUFACTURING,
    "ICT": Category.SOFTWARE,
    "HLT": Category.HEALTHCARE,
    "HSP": Category.FOOD,
    "CON": Category.CONSTRUCTION,
    "FIN": Category.FINANCE,
    "EDU": Category.EDUCATION,
}

LEGAL_SUFFIXES = (" Pty Ltd", " Ltd", " Limited")


def company_from_listing(listing):
    """Translate one Tradeline listing into a Company.

    Unknown sector codes become "no hint", never a guessed category.
    """
    name = listing["trading_name"]
    for suffix in LEGAL_SUFFIXES:
        name = name.removesuffix(suffix)
    return Company(
        company_id=f"tradeline:{listing['listing_id']}",
        name=name,
        directory_hint=SECTOR_CODE_TO_CATEGORY.get(listing.get("sector_code")),
    )
