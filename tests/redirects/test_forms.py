"""Test `redirects.forms` module."""
from django import forms
from django.test.client import RequestFactory

import pytest
from crispy_forms.helper import FormHelper

from redirects.forms import RedirectModelForm
from redirects.models import Redirect


class TestRedirectModelForm:
    """Test `RedirectModelForm` form."""

    form_class = RedirectModelForm
    model_class = Redirect

    @pytest.fixture()
    def redirect_form(self, rf: RequestFactory, db: None) -> RedirectModelForm:
        """Initialize `RedirectModelForm` form."""
        request = rf.get("/")
        return RedirectModelForm(request=request)

    def test_inheritance(self) -> None:
        """Inherits from Django's `ModelForm`."""
        assert issubclass(self.form_class, forms.BaseForm)
        assert issubclass(self.form_class, forms.ModelForm)

    def test_form_model(self, redirect_form: RedirectModelForm) -> None:
        """Is a model form for `redirects.Redirect`."""
        assert redirect_form._meta.model == self.model_class

    def test_form_helper(self, redirect_form: RedirectModelForm) -> None:
        """Has a `crispy_forms.FormHelper` integration."""
        assert isinstance(redirect_form.helper, FormHelper)

    @pytest.mark.django_db()
    def test_invalid_local_path(
        self, rf: RequestFactory, invalid_local_path: str
    ) -> None:
        """Fails validation for incorrect `local_path` values."""
        data = {
            "local_path": invalid_local_path,
            "destination_url": "https://example.com/",
        }
        request = rf.get("/")
        form = self.form_class(data, request=request)

        assert not form.is_valid()
        assert "local_path" in form.errors

    @pytest.mark.django_db()
    def test_unique_local_path(self, rf: RequestFactory) -> None:
        """Fails validation for not unique `local_path` values."""
        data = {
            "local_path": "foo/bar.html",
            "destination_url": "https://example.com/",
        }
        request = rf.get("/")
        form = self.form_class(data, request=request)

        assert form.is_valid()
        form.save()

        form = self.form_class(data, request=request)
        assert not form.is_valid()
        assert "local_path" in form.errors

    @pytest.mark.django_db()
    def test_invalid_destination_url(
        self, rf: RequestFactory, invalid_destination_url: str
    ) -> None:
        """Fails validation for incorrect `destination_url` values."""
        data = {
            "local_path": "foo/bar.html",
            "destination_url": invalid_destination_url,
        }
        request = rf.get("/")
        form = self.form_class(data, request=request)

        assert not form.is_valid()
        assert "destination_url" in form.errors

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        ("local_path", "destination_url"),
        [
            ("foo/bar.html", "https://youtu.be/I6OXjnBIW-4"),
            ("2023/01/01/good-news-everyone", "https://pawelad.me/"),
        ],
    )
    def test_form_valid(
        self, rf: RequestFactory, local_path: str, destination_url: str
    ) -> None:
        """Requires valid `local_path` and `destination_url` fields."""
        data = {
            "local_path": local_path,
            "destination_url": destination_url,
        }
        request = rf.get("/")
        form = self.form_class(data, request=request)
        assert form.is_valid()

    @pytest.mark.django_db()
    def test_form_save(self, rf: RequestFactory) -> None:
        """Creates `Redirect` on save."""
        data = {
            "local_path": "foo/bar.html",
            "destination_url": "https://example.com/",
        }
        request = rf.get("/")
        form = self.form_class(data, request=request)
        assert form.is_valid()

        form.save()

        redirect = self.model_class.objects.get(local_path=data["local_path"])
        assert redirect
        assert redirect.destination_url == data["destination_url"]
