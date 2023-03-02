"""Shared fakester test fixtures."""
import pytest
from fakeredis import FakeRedis, FakeStrictRedis
from pytest_django.fixtures import SettingsWrapper
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def _enable_whitenoise_autorefresh(settings: SettingsWrapper) -> None:
    """Enable `WHITENOISE_AUTOREFRESH` setting to get rid of "No directory at" warning.

    Related:
        - https://github.com/evansd/whitenoise/issues/191
        - https://github.com/evansd/whitenoise/issues/215
        - https://github.com/evansd/whitenoise/commit/4204494d44213f7a51229de8bc224cf6d84c01eb
    """  # noqa: E501
    settings.WHITENOISE_AUTOREFRESH = True


@pytest.fixture(autouse=True)
def _use_fake_redis(mocker: MockerFixture) -> None:
    """Use `fakeredis` in all tests."""
    mocker.patch("redis.Redis", FakeRedis)
    mocker.patch("redis.StrictRedis", FakeStrictRedis)

    # This is needed because Django's `RedisCacheClient` imports `redis` module
    # inside its init function
    _redis_module = mocker.MagicMock(name="redis_mock")
    _redis_module.Redis = FakeRedis
    _redis_module.StrictRedis = FakeStrictRedis
    mocker.patch.dict("sys.modules", {"redis": _redis_module})
