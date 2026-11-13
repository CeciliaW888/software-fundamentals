"""Retries with backoff for temporary website failures (Day 24)."""
import time

from enricher.core.ports import SourceDown, TemporaryWebsiteError


def retry_with_backoff(call, attempts=3, base_delay_seconds=0.2, sleep=time.sleep):
    """Run call(); after a TemporaryWebsiteError wait and try again.

    Waits base_delay, then 2 x base_delay, and so on. Any other error is
    not retried. After the last attempt, raises SourceDown.
    """
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except TemporaryWebsiteError as error:
            if attempt == attempts:
                raise SourceDown(str(error)) from error
            sleep(base_delay_seconds * 2 ** (attempt - 1))


class RetryingWebsiteSource:
    def __init__(self, inner, attempts=3, base_delay_seconds=0.2, sleep=time.sleep):
        self._inner = inner
        self._attempts = attempts
        self._base_delay_seconds = base_delay_seconds
        self._sleep = sleep

    def about_page(self, company_name):
        return retry_with_backoff(
            lambda: self._inner.about_page(company_name),
            attempts=self._attempts,
            base_delay_seconds=self._base_delay_seconds,
            sleep=self._sleep,
        )
