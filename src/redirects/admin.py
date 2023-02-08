"""
Redirects application Django Admin integration.
"""
from django.contrib import admin

from redirects.models import Redirect


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    """Django Admin integration for `redirects.Redirect` model."""

    list_display = (
        "pk",
        "local_path",
        "destination_url",
        "views",
        "sender_ip",
        "created_at",
        "modified_at",
    )

    list_filter = (
        "sender_ip",
        "created_at",
        "modified_at",
    )

    ordering = (
        "modified_at",
        "created_at",
    )

    search_fields = (
        "local_path",
        "destination_url",
    )
