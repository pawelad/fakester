"""
Redirects module models
"""
import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class Redirect(TimeStampedModel, models.Model):
    """
    Model that represents a single redirect
    """
    local_path = models.CharField(
        verbose_name=_("local path"),
        max_length=256,
        unique=True,
        validators=[RegexValidator(
            regex='[a-zA-Z0-9/._-]+',
            message=_("Allowed characters: a-z, A-Z, 0-9, slash (/), "
                      "dot (.), underscore (_) and hyphen (-)."),
        )],
        error_messages={
            'unique': _("Sorry, but this path is already taken.")
        },
    )

    destination_url = models.URLField(
        verbose_name=_("destination url"),
    )

    clicks = models.PositiveIntegerField(
        verbose_name=_("clicks"),
        default=0,
        editable=False,
    )

    sender_ip = models.GenericIPAddressField(
        verbose_name=_("sender IP"),
        null=True,
        editable=False,
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("redirect")
        verbose_name_plural = _("redirects")

    def __str__(self):
        return (
            "Redirect from {0.local_path} to {0.destination_url}".format(self)
        )

    def clean(self):
        """
        Extends Django's default `clean()` method and add simple local path
        cleaning
        """
        # Remove leading slashes in local path
        self.local_path = self.local_path.lstrip('/')

        # Remove multiple slash characters in a row
        self.local_path = re.sub('/+', '/', self.local_path)

        return super().clean()
