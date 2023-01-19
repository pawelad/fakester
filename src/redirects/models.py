"""
Redirects module models.
"""
import re

from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class Redirect(BaseModel):
    """
    Model that represents a single redirect.
    """

    local_path = models.SlugField(
        verbose_name=_("local path"),
        max_length=255,
        unique=True,
        error_messages={"unique": _("Sorry, but this path is already taken.")},
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

    class Meta:
        verbose_name = _("redirect")
        verbose_name_plural = _("redirects")

    def __str__(self):
        return "Redirect from {0.local_path} to {0.destination_url}".format(self)

    def clean(self):
        """
        Extends Django's default `clean()` method and add simple local path
        cleaning.
        """
        # Remove leading slashes in local path
        self.local_path = self.local_path.lstrip("/")

        # Remove multiple slash characters in a row
        self.local_path = re.sub("/+", "/", self.local_path)

        return super().clean()
