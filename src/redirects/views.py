"""Redirects app views."""
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django_ratelimit.decorators import ratelimit
from ipware import get_client_ip

from redirects.forms import RedirectModelForm
from redirects.models import Redirect


class RedirectFormView(TemplateView):
    """Redirect creation form view."""

    template_name = "redirects/form.html"
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add available domains and initialised form to the template."""
        kwargs["available_domains"] = settings.AVAILABLE_DOMAINS
        kwargs["form"] = RedirectModelForm(
            data=self.request.POST or None,
            request=self.request,
        )

        return super().get_context_data(**kwargs)

    @method_decorator(ratelimit(key="ip", rate="3/m"))
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """Handle redirect form saving and default to GET response."""
        ctx = self.get_context_data(**kwargs)

        form = ctx["form"]
        if form.is_valid():
            # Add sender IP address
            redirect = form.save(commit=False)
            redirect.sender_ip, _ = get_client_ip(self.request)
            redirect.save()

            # Add saved object to view in order to access it in the template
            self.redirect = redirect

        return super().get(request, *args, **kwargs)


class RedirectToDestinationView(TemplateView):
    """Redirect user to destination URL view."""

    template_name = "redirects/redirect_to_destination.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Increase redirect view count and redirect user to destination URL."""
        redirect = get_object_or_404(
            Redirect,
            local_path=self.kwargs["local_path"],
        )
        redirect.increase_view_count()

        kwargs["redirect"] = redirect

        return super().get_context_data(**kwargs)
