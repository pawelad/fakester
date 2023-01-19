"""
fakester main URLs config.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # Misc
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # Django Admin
    path("admin/", admin.site.urls),
    # Apps
    path("", include("redirects.urls", namespace="redirects")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
