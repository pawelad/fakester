"""Test `redirects.models` module."""

from django.core.exceptions import ValidationError
from django.db import models
from django.test.client import RequestFactory

import pytest
from model_bakery import baker
from pytest_django.fixtures import SettingsWrapper

from redirects.models import Redirect
from utils.models import BaseModel


class TestRedirect:
    """Test `Redirect` model."""

    model_class = Redirect

    def test_inheritance(self) -> None:
        """Inherits from Django's `Model`."""
        assert issubclass(self.model_class, BaseModel)
        assert issubclass(self.model_class, models.Model)

    def test_str(self, redirect: Redirect) -> None:
        """Contains model primary key, `local_path` and `destination_url` fields."""
        redirect_str = str(redirect)

        assert str(redirect.pk) in redirect_str
        assert redirect.local_path in redirect_str
        assert redirect.destination_url in redirect_str

    def test_clean(self) -> None:
        """Leading slashes from `local_path` field are removed."""
        data = {
            "local_path": "//this_is/////a//local_path",
            "destination_url": "https://example.com/",
        }
        redirect = self.model_class(**data)
        redirect.clean()

        assert redirect.local_path == "this_is/////a//local_path"
        assert redirect.destination_url == "https://example.com/"

    def test_increase_view_count(self, redirect: Redirect) -> None:
        """Redirect view count is increased."""
        assert redirect.views == 0

        redirect.increase_view_count()
        redirect.refresh_from_db()
        assert redirect.views == 1

        redirect.increase_view_count()
        redirect.refresh_from_db()
        assert redirect.views == 2

        redirect.increase_view_count()
        redirect.refresh_from_db()
        assert redirect.views == 3

    @pytest.mark.django_db()
    def test_invalid_local_path(self, invalid_local_path: str) -> None:
        """Fails validation for incorrect `local_path` values."""
        redirect = baker.make(self.model_class, local_path=invalid_local_path)

        with pytest.raises(ValidationError, match="local_path"):
            redirect.full_clean()

    @pytest.mark.django_db()
    def test_invalid_destination_url(self, invalid_destination_url: str) -> None:
        """Fails validation for incorrect `destination_url` values."""
        redirect = baker.make(self.model_class, destination_url=invalid_destination_url)

        with pytest.raises(ValidationError, match="destination_url"):
            redirect.full_clean()

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        ("local_path", "destination_url"),
        [
            ("foo/bar/baz.html", "https://youtu.be/I6OXjnBIW-4"),
            ("2023/01/01/good-news-everyone", "https://pawelad.me/"),
        ],
    )
    def test_model_valid(self, local_path: str, destination_url: str) -> None:
        """Requires valid `local_path` and `destination_url` fields."""
        redirect = baker.make(
            self.model_class,
            local_path=local_path,
            destination_url=destination_url,
        )

        redirect.full_clean()

    @pytest.mark.django_db()
    def test_model_save(self) -> None:
        """Creates `Redirect` on save."""
        data = {
            "local_path": "foo/bar/baz.html",
            "destination_url": "https://youtu.be/I6OXjnBIW-4",
        }
        redirect = self.model_class(**data)
        redirect.full_clean()
        redirect.save()

        redirect = self.model_class.objects.get(local_path=data["local_path"])
        assert redirect
        assert redirect.destination_url == data["destination_url"]

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        ("local_path", "available_domains", "fakester_links"),
        [
            ("pawelad.html", None, ["http://localhost/pawelad.html"]),
            (
                "local_path",
                ["example.com", "foo.bar"],
                [
                    "http://localhost/local_path",
                    "http://example.com/local_path",
                    "http://foo.bar/local_path",
                ],
            ),
            (
                "with/a/slash",
                ["example.com", "foo.bar", "localhost"],
                [
                    "http://localhost/with/a/slash",
                    "http://example.com/with/a/slash",
                    "http://foo.bar/with/a/slash",
                ],
            ),
        ],
    )
    def test_get_fakester_links(
        self,
        settings: SettingsWrapper,
        rf: RequestFactory,
        redirect: Redirect,
        local_path: str,
        available_domains: list[str],
        fakester_links: list[str],
    ) -> None:
        """Creates all fakester links based on available domains."""
        settings.ALLOWED_HOSTS = ["localhost"]
        settings.AVAILABLE_DOMAINS = available_domains

        data = {
            "local_path": local_path,
            "destination_url": "https://youtu.be/I6OXjnBIW-4",
        }
        redirect = self.model_class(**data)
        redirect.full_clean()
        redirect.save()

        request = rf.get(f"/{local_path}", HTTP_HOST="localhost")

        assert redirect.get_fakester_links(request) == fakester_links
