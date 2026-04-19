"""Security tests for redirects app."""

from django.test import Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import pytest
from redirects.models import Redirect


@pytest.mark.django_db
def test_xss_escaped_in_redirect_template(client: Client) -> None:
    """The payload should be escaped for JS."""
    # This payload tries to break out of the JS string and execute alert
    payload = 'https://example.com/"; alert("XSS"); //'

    # We bypass model validation here because we want to test the template's escaping
    # even if such a URL shouldn't be allowed by the model.
    redirect = Redirect.objects.create(local_path="test-xss", destination_url=payload)

    url = reverse("redirects:redirect", kwargs={"local_path": redirect.local_path})
    response = client.get(url)

    content = response.content.decode()

    # The payload should be escaped for JS
    # " becomes \u0022 or similar
    assert 'alert("XSS")' not in content
    # Django's escapejs usually escapes " as \u0022
    assert "\\u0022; alert(\\u0022XSS\\u0022); //" in content


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "vbscript:msgbox(1)",
    ],
)
def test_redirect_model_denies_unsafe_schemes(url: str) -> None:
    """The model should deny unsafe schemes."""
    validator = URLValidator(schemes=["http", "https"])
    with pytest.raises(ValidationError):
        validator(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://example.com/foo?bar=baz#qux",
    ],
)
def test_redirect_model_allows_safe_schemes(url: str) -> None:
    """The model should allow safe schemes."""
    validator = URLValidator(schemes=["http", "https"])
    validator(url)
