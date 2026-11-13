"""Where accepted results are kept. In memory until Module 5."""


class InMemoryResultStore:
    def __init__(self):
        self.saved_results = []

    def save(self, result):
        self.saved_results.append(result)
