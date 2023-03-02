"""Redirects app models."""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from utils.models import BaseModel


class Redirect(BaseModel):
    """Single redirect model representation."""

    local_path = models.CharField(
        verbose_name="local path",
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9/._-]+$",
                message=(
                    "Allowed characters: a-z, A-Z, 0-9, slash (/), dot (.), "
                    "underscore (_) and hyphen (-)."
                ),
            ),
        ],
        error_messages={"unique": "This path is already taken."},
    )

    destination_url = models.URLField(
        verbose_name="destination URL",
    )

    views = models.PositiveIntegerField(
        verbose_name="views",
        default=0,
        editable=False,
    )

    sender_ip = models.GenericIPAddressField(
        verbose_name="sender IP",
        null=True,
        editable=False,
    )

    class Meta:
        verbose_name = "redirect"
        verbose_name_plural = "redirects"

    def __str__(self) -> str:
        """Return a human-readable redirect name."""
        return (
            f"Redirect from '{self.local_path}' to '{self.destination_url}' "
            f"(ID: {self.pk})"
        )

    def clean(self) -> None:
        """Sanitize `local_path` value and check for forbidden values."""
        # Remove leading slashes from local path
        self.local_path = self.local_path.lstrip("/")

        if self.local_path in {
            "favicon.ico",
            "robots.txt",
            "humans.txt",
            "ads.txt",
            "sellers.json",
        }:
            raise ValidationError({"local_path": "Path is not allowed."})

        for path_prefix in ("_/", ".well-known/"):
            if self.local_path.startswith(path_prefix):
                raise ValidationError(
                    {"local_path": f"Path cannot start with '{path_prefix}'."}
                )

        return super().clean()

    def get_absolute_url(self) -> str:
        """Return redirect URL."""
        from django.urls import reverse

        return reverse("redirects:redirect", kwargs={"local_path": self.local_path})

    def increase_view_count(self) -> None:
        """Increase redirect view count by 1."""
        self.views += 1
        self.save()
