"""Keeps results in memory. Tests use it; production uses SqliteResultStore."""


class InMemoryResultStore:
    def __init__(self):
        self.saved_results = []

    def save(self, result):
        self.saved_results.append(result)
