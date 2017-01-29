"""
Redirects module urls config
"""

from django.conf.urls import url

from redirects import views


urlpatterns = [
    url(r'^$', views.RedirectFormView.as_view(), name='form'),

    url(
        r'^(?P<local_path>[a-zA-Z0-9/._-]+)$',
        views.ActualRedirectView.as_view(),
        name='redirect'
    ),
]
