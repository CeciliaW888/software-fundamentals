"""Everything the service knows about categories lives here.

Adding a category is one edit in this file.
"""

OTHER = "Other"

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
}

CATEGORIES = [*CATEGORY_KEYWORDS, OTHER]

MINIMUM_CONFIDENCE = 0.82
