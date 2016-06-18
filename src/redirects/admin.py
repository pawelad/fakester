from django.contrib import admin

from redirects.models import Redirect


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('local_path', 'destination_url', 'clicks', 'sender_ip')
