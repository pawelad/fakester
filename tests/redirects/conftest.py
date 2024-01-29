"""Redirect app test fixtures."""

import pytest
from _pytest.fixtures import SubRequest
from model_bakery import baker

from redirects.models import Redirect


@pytest.fixture()
def redirect(db: None) -> Redirect:
    """Initialize `Redirect` model."""
    return baker.make(Redirect)


INVALID_LOCAL_PATHS = (
    "favicon.ico",
    "robots.txt",
    "humans.txt",
    "/ads.txt",
    "/sellers.json",
    "_/admin/",
    "/_/foobar.html",
    ".well-known/",
    ".well-known/secret.html",
    "SELECT * FROM foobar",
)


@pytest.fixture(params=INVALID_LOCAL_PATHS)
def invalid_local_path(request: SubRequest) -> str:
    """Parametrized fixture that returns invalid values for `local_path` field."""
    return request.param


INVALID_DESTINATION_URLS = (
    "_/admin/",
    "not an URL",
    "SELECT * FROM foobar",
)


@pytest.fixture(params=INVALID_DESTINATION_URLS)
def invalid_destination_url(request: SubRequest) -> str:
    """Parametrized fixture that returns invalid values for `destination_url` field."""
    return request.param
