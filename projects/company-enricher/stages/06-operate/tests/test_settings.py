import pytest

from enricher.settings import Settings


def test_defaults_when_nothing_is_set():
    settings = Settings.from_env({})
    assert settings.minimum_confidence == 0.82
    assert settings.use_http_source is False


def test_values_come_from_the_environment():
    settings = Settings.from_env({"ENRICHER_MIN_CONFIDENCE": "0.9", "ENRICHER_USE_HTTP_SOURCE": "true"})
    assert settings.minimum_confidence == 0.9
    assert settings.use_http_source is True


@pytest.mark.parametrize("environ", [{"ENRICHER_MIN_CONFIDENCE": "1.5"}, {"ENRICHER_RETRY_ATTEMPTS": "0"}])
def test_bad_values_stop_the_service_at_startup(environ):
    with pytest.raises(ValueError):
        Settings.from_env(environ)
