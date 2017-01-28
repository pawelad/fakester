import re

from django.core.validators import RegexValidator
from django.db import models

import pytest
from django_extensions.db.models import TimeStampedModel

from redirects.models import Redirect


class TestRedirectModel:
    """
    Tests for 'redirects.models.Redirect'
    """
    model = Redirect

    def test_model_inheritance(self):
        """Test model inheritance"""
        assert isinstance(self.model(), models.Model)
        assert isinstance(self.model(), TimeStampedModel)

    def test_model_local_path_field(self):
        """Test model 'local_path' field"""
        field = self.model._meta.get_field('local_path')

        assert isinstance(field, models.CharField)
        assert field.verbose_name == 'local path'
        assert field.max_length == 256
        assert field.unique
        assert (
            field.error_messages['unique'] ==
            "Sorry, but this path is already taken."
        )

    def test_model_local_path_field_validator(self):
        """Test model 'local_path' field `RegexValidator`"""
        instance = self.model()
        field = instance._meta.get_field('local_path')
        validator = field.validators[0]

        assert isinstance(validator, RegexValidator)
        assert validator.regex == re.compile('[a-zA-Z0-9/._-]+')
        assert (
            validator.message ==
            "Allowed characters: a-z, A-Z, 0-9, slash (/), dot (.), "
            "underscore (_) and hyphen (-)."
        )

    def test_model_destination_url_field(self):
        """Test model 'destination_url' field"""
        field = self.model._meta.get_field('destination_url')

        assert isinstance(field, models.URLField)
        assert field.verbose_name == 'destination url'

    def test_model_clicks_field(self):
        """Test model 'clicks' field"""
        field = self.model._meta.get_field('clicks')

        assert isinstance(field, models.PositiveIntegerField)
        assert field.verbose_name == 'clicks'
        assert field.default == 0
        assert not field.editable

    def test_model_sender_ip_field(self):
        """Test model 'sender_ip' field"""
        field = self.model._meta.get_field('sender_ip')

        assert isinstance(field, models.GenericIPAddressField)
        assert field.verbose_name == 'sender IP'
        assert field.null
        assert not field.editable

    def test_model_meta_class(self):
        """Test model `Meta` class"""
        meta = self.model._meta

        assert self.model.Meta is TimeStampedModel.Meta
        assert meta.verbose_name == 'redirect'
        assert meta.verbose_name_plural == 'redirects'

    @pytest.mark.django_db
    def test_model_clean_method(self):
        """Test model `clean()` method"""
        redirect = Redirect(
            local_path='//this_is/////a//local_path',
            destination_url='http://example.com',
        )

        redirect.full_clean()

        assert redirect.local_path == 'this_is/a/local_path'

    @pytest.mark.django_db
    def test_model_str_method(self, redirect):
        """Test model string representation"""
        assert redirect.local_path in str(redirect)
        assert redirect.destination_url in str(redirect)
