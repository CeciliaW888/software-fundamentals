"""The category list and the words that signal each category."""
from enum import Enum


class Category(Enum):
    RETAIL = "Retail"
    WHOLESALE = "Wholesale & Distribution"
    MANUFACTURING = "Manufacturing"
    SOFTWARE = "Software & IT"
    HEALTHCARE = "Healthcare"
    FOOD = "Food & Hospitality"
    CONSTRUCTION = "Construction"
    FINANCE = "Finance"
    EDUCATION = "Education"
    OTHER = "Other"


CATEGORY_KEYWORDS = {
    Category.RETAIL: {"store", "shop", "sells", "retail", "boutique"},
    Category.WHOLESALE: {"wholesale", "distribute", "distribution", "bulk", "warehouse"},
    Category.MANUFACTURING: {"manufacture", "manufacturing", "factory", "fabricate", "bake"},
    Category.SOFTWARE: {"software", "cloud", "technology", "apps", "hosting"},
    Category.HEALTHCARE: {"clinic", "patients", "dental", "medical", "health"},
    Category.FOOD: {"restaurant", "cafe", "cafes", "catering", "breakfast", "lunch", "dinner", "bread", "pastries"},
    Category.CONSTRUCTION: {"build", "homes", "renovate", "construction", "builders"},
    Category.FINANCE: {"loans", "lending", "insurance", "banking", "accounting"},
    Category.EDUCATION: {"teach", "courses", "students", "exam", "school"},
}
