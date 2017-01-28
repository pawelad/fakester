from django.urls import reverse_lazy
from django.views.generic import TemplateView

import pytest
from ratelimit.mixins import RatelimitMixin

from redirects.forms import RedirectModelForm
from redirects.models import Redirect
from redirects.views import RedirectFormView


class TestRedirectFormView:
    """
    Tests for 'redirects.views.RedirectFormView'
    """
    view = RedirectFormView
    url = reverse_lazy('redirects:form')

    def test_view_inheritance(self):
        """Test view inheritance name"""
        assert isinstance(self.view(), TemplateView)
        assert isinstance(self.view(), RatelimitMixin)

    def test_view_url_reversing(self):
        """Test view URL reversing"""
        assert str(self.url) == '/'

    def test_view_template(self):
        """Test view template name"""
        assert self.view.template_name == 'redirects/form.html'

    def test_view_ratelimit_config(self):
        """Test view 'django-ratelimit' config"""
        assert self.view.ratelimit_key == 'ip'
        assert self.view.ratelimit_rate == '5/m'
        assert self.view.ratelimit_block

    def test_view_allowed_methods(self):
        """Test view allowed methods"""
        assert set(self.view.http_method_names) == {'get', 'post'}

    def test_view_rendering(self, client):
        """Test view rendering"""
        response = client.get(self.url)

        assert response.status_code == 200

        assert 'form' in response.context
        assert isinstance(response.context['form'], RedirectModelForm)

    @pytest.mark.django_db
    def test_view_redirect_creation(self, monkeypatch, faker, mocker, client):
        """Test creating a new `Redirect` instance with the view"""
        monkeypatch.setenv('RECAPTCHA_TESTING', 'True')

        ip_address = faker.ipv4()
        mocker.patch('redirects.views.get_real_ip', return_value=ip_address)

        data = {
            'local_path': faker.uri_path(),
            'destination_url': faker.uri(),
            'g-recaptcha-response': 'PASSED',
        }

        response = client.post(self.url, data)

        assert response.status_code == 200
        assert hasattr(response.context['view'], 'redirect')
        assert isinstance(response.context['view'].redirect, Redirect)

        redirect = response.context['view'].redirect
        assert redirect.local_path == data['local_path']
        assert redirect.destination_url == data['destination_url']
        assert redirect.sender_ip == ip_address
