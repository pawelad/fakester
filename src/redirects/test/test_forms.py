from django import forms

import pytest

from redirects.forms import RedirectModelForm
from redirects.models import Redirect


# Fixtures
@pytest.fixture(scope='module')
def redirect_form():
    """Helper fixture for initializing `RedirectModelForm`"""
    return RedirectModelForm()


# Tests
class TestRedirectModelForm:
    """
    Tests for 'redirects.forms.RedirectModelForm'
    """
    def test_from_inheritance(self, redirect_form):
        """Form should inherit from `django.forms.ModelForm`"""
        assert isinstance(redirect_form, forms.ModelForm)

    def test_from_model(self, redirect_form):
        """Form model should be `redirects.models.Redirect`"""
        assert redirect_form._meta.model == Redirect

    def test_form_local_path_field(self, redirect_form):
        """Form should have a 'local_path' field"""
        assert 'local_path' in redirect_form.fields

        field = redirect_form.fields['local_path']

        assert isinstance(field, forms.CharField)
        assert isinstance(field.widget, forms.TextInput)
        assert field.label == 'Fake local path'
        assert (
            field.widget.attrs['placeholder'] ==
            '/2016/06/23/fakester-is-the-new-cool-thing.html'
        )

    def test_form_destination_url_field(self, redirect_form):
        """Form should have a 'destination_url' field"""
        assert 'destination_url' in redirect_form.fields

        field = redirect_form.fields['destination_url']

        assert isinstance(field, forms.CharField)
        assert isinstance(field.widget, forms.TextInput)
        assert field.label == 'Destination URL'
        assert (
            field.widget.attrs['placeholder'] ==
            'https://github.com/pawelad/fakester'
        )
