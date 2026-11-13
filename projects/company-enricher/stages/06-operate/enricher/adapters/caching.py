"""Remember About pages already read in this run (Day 23).

Measured first: reading the website is the slowest step, and batches often
repeat a company. Only successful pages are cached.
"""


class CachingWebsiteSource:
    def __init__(self, inner):
        self._inner = inner
        self._pages = {}

    def about_page(self, company_name):
        if company_name not in self._pages:
            self._pages[company_name] = self._inner.about_page(company_name)
        return self._pages[company_name]
