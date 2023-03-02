"""Redirects app URLs config."""
from django.urls import path, re_path

from redirects import views

app_name = "redirects"

urlpatterns = [
    path("", views.RedirectFormView.as_view(), name="form"),
    re_path(
        # Select everything, except for private `_/` and `.well-known/` paths
        r"^(?!_/|.well-known/)(?P<local_path>[a-zA-Z0-9/._-]+)$",
        views.ActualRedirectView.as_view(),
        name="redirect",
    ),
]
