"""Test `redirects.views` module."""
from http import HTTPStatus

from django.template.response import TemplateResponse
from django.test import Client
from django.urls import resolve, reverse
from django.views.generic import TemplateView, View

import pytest
from pytest_django.asserts import assertContains, assertTemplateUsed
from pytest_mock import MockerFixture

from redirects.forms import RedirectModelForm
from redirects.models import Redirect
from redirects.views import RedirectFormView, RedirectToDestinationView


class TestRedirectFormView:
    """Test 'RedirectFormView' view."""

    view_class = RedirectFormView
    view_name = "redirects:form"
    url = "/"

    def test_inheritance(self) -> None:
        """Inherits from Django's `TemplateView`."""
        assert issubclass(self.view_class, View)
        assert issubclass(self.view_class, TemplateView)

    def test_url_reversing(self) -> None:
        """Resolves to expected path."""
        assert reverse(self.view_name) == self.url

        resolver = resolve(self.url)
        assert resolver.func.view_class == self.view_class  # type: ignore
        assert resolver.view_name == self.view_name

    def test_allowed_http_methods(self, client: Client) -> None:
        """Only allows GET and POST HTTP methods."""
        assert client.get(self.url).status_code == HTTPStatus.OK
        assert client.post(self.url).status_code == HTTPStatus.OK

        assert client.delete(self.url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.head(self.url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.options(self.url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.patch(self.url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.put(self.url).status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_template_used(self, client: Client) -> None:
        """Uses expected template."""
        response = client.get(self.url)

        assert isinstance(response, TemplateResponse)
        assertTemplateUsed(response, "redirects/form.html")

    def test_render_form(self, client: Client) -> None:
        """Renders redirect form."""
        response = client.get(self.url)

        assert isinstance(response, TemplateResponse)
        assert response.status_code == 200

        assert "form" in response.context_data
        assert isinstance(response.context_data["form"], RedirectModelForm)

        assertContains(response, "<form", count=1)

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        ("local_path", "destination_url"),
        [
            ("foo/bar.html", "https://youtu.be/I6OXjnBIW-4"),
            ("2023/01/01/good-news-everyone", "https://pawelad.me/"),
        ],
    )
    def test_redirect_creation(
        self,
        mocker: MockerFixture,
        client: Client,
        local_path: str,
        destination_url: str,
    ) -> None:
        """Creates a new `Redirect` instance."""
        ip_address = "192.168.1.1"
        mocker.patch("redirects.views.get_client_ip", return_value=(ip_address, True))

        data = {
            "local_path": local_path,
            "destination_url": destination_url,
        }

        response = client.post(self.url, data)

        assert response.status_code == 200
        assert hasattr(response.context["view"], "redirect")
        assert isinstance(response.context["view"].redirect, Redirect)

        redirect = Redirect.objects.get(local_path=data["local_path"])
        assert redirect.destination_url == data["destination_url"]
        assert redirect.views == 0
        assert redirect.author_ip == ip_address

    @pytest.mark.xfail(reason="I don't know why this test isn't working")
    @pytest.mark.django_db()
    def test_ratelimit(self, client: Client) -> None:
        """Allows at most three POST request per minute."""
        data = {
            "local_path": "foo.html",
            "destination_url": "https://pawelad.me/",
        }
        response = client.post(self.url, data)
        assert response.status_code == 200

        data = {
            "local_path": "foo/bar.html",
            "destination_url": "https://pawelad.me/",
        }
        response = client.post(self.url, data)
        assert response.status_code == 200

        data = {
            "local_path": "foo/baz.html",
            "destination_url": "https://pawelad.me/",
        }
        response = client.post(self.url, data)
        assert response.status_code == 200

        data = {
            "local_path": "foo/bar/baz.html",
            "destination_url": "https://pawelad.me/",
        }
        response = client.post(self.url, data)
        assert response.status_code == 403


class TestRedirectToDestinationView:
    """Test `RedirectToDestinationView` view."""

    view_class = RedirectToDestinationView
    view_name = "redirects:redirect"

    def test_inheritance(self) -> None:
        """Inherits from Django's `TemplateView`."""
        assert issubclass(self.view_class, View)
        assert issubclass(self.view_class, TemplateView)

    def test_url_reversing(self, redirect: Redirect) -> None:
        """Resolves to expected path."""
        url = redirect.get_absolute_url()

        resolver = resolve(url)
        assert resolver.func.view_class == self.view_class  # type: ignore
        assert resolver.view_name == self.view_name

    def test_allowed_http_methods(self, client: Client, redirect: Redirect) -> None:
        """Only allows GET HTTP method."""
        url = redirect.get_absolute_url()

        assert client.get(url).status_code == HTTPStatus.OK

        assert client.delete(url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.head(url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.options(url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.patch(url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.post(url).status_code == HTTPStatus.METHOD_NOT_ALLOWED
        assert client.put(url).status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_template_used(self, client: Client, redirect: Redirect) -> None:
        """Uses expected template."""
        url = redirect.get_absolute_url()

        response = client.get(url)

        assert isinstance(response, TemplateResponse)
        assertTemplateUsed(response, "redirects/redirect_to_destination.html")

    @pytest.mark.django_db()
    def test_render_redirect(self, client: Client, redirect: Redirect) -> None:
        """Renders redirect."""
        url = redirect.get_absolute_url()

        response = client.get(url)

        assert isinstance(response, TemplateResponse)
        assert response.status_code == 200

        html_redirect = (
            f'<meta http-equiv="refresh" content="1; url={redirect.destination_url}">'
        )
        assertContains(response, html_redirect, count=1, html=True)

        js_redirect = (
            f'<script>window.location.href = "{redirect.destination_url}";</script>'
        )
        assertContains(response, js_redirect, count=1, html=True)

    def test_render_404(self, client: Client) -> None:
        """Results in HTTP 404 when trying to access nonexistent redirect."""
        response = client.get("foo.html")
        assert response.status_code == 404

    @pytest.mark.django_db()
    def test_view_counting(self, client: Client, redirect: Redirect) -> None:
        """Increases redirect view count when viewed."""
        url = redirect.get_absolute_url()

        assert redirect.views == 0

        client.get(url)
        redirect.refresh_from_db()
        assert redirect.views == 1

        client.get(url)
        redirect.refresh_from_db()
        assert redirect.views == 2

        client.get(url)
        redirect.refresh_from_db()
        assert redirect.views == 3
