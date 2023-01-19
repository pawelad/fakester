"""
Redirects module Django Admin integration.
"""
from django.contrib import admin

from redirects.models import Redirect


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    """
    Django Admin integration for `redirects.Redirect` model.
    """

    list_display = (
        "local_path",
        "destination_url",
        "clicks",
        "sender_ip",
        "created_at",
        "modified_at",
    )
    list_filter = ("sender_ip", "destination_url")
