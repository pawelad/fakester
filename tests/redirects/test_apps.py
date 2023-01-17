"""
Test `redirects.apps` file
"""
from django.apps import AppConfig
from django.apps import apps as fakester_apps


def test_redirects_app_config():
    """Test 'redirects' module `AppConfig` instance"""
    redirects_app_config = fakester_apps.get_app_config("redirects")

    assert isinstance(redirects_app_config, AppConfig)
    assert redirects_app_config.name == "redirects"
    assert redirects_app_config.verbose_name == "redirects"
