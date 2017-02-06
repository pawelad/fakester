"""
Fakester application main urls config
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^robots\.txt$', TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain')
        ),

    # Django Admin
    url(r'^django_admin/', admin.site.urls),

    # Redirects
    url(r'', include('redirects.urls', namespace='redirects')),
]

# Serve static files on runserver
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
