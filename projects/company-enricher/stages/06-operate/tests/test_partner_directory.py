from enricher.adapters.partner_directory import company_from_listing
from enricher.core.categories import Category


def test_translates_a_listing_into_our_company():
    listing = {"listing_id": "TL-0042", "trading_name": "Saltwater Kitchen Pty Ltd", "sector_code": "HSP"}

    company = company_from_listing(listing)

    assert company.company_id == "tradeline:TL-0042"
    assert company.name == "Saltwater Kitchen"
    assert company.directory_hint is Category.FOOD


def test_unknown_sector_code_gives_no_hint():
    listing = {"listing_id": "TL-0099", "trading_name": "Quiet Hours Studio", "sector_code": "ZZZ"}
    assert company_from_listing(listing).directory_hint is None
