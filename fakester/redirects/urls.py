"""
Redirects app urls config.
"""
from django.urls import path

from redirects import views

app_name = "redirects"

urlpatterns = [
    path("", views.RedirectFormView.as_view(), name='form'),
    path("<slug:local_path>", views.ActualRedirectView.as_view(), name='redirect'),
]
