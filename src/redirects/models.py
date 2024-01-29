"""Redirects app models."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.http import HttpRequest

from yarl import URL

from utils.misc import deslugify
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

    title = models.CharField(
        verbose_name="title",
        max_length=255,
        default="",
        blank=True,
        help_text=(
            "Used in link previews. If not provided, it will be automatically "
            "generated."
        ),
    )

    description = models.TextField(
        verbose_name="description",
        default="",
        blank=True,
        help_text="Used in link previews.",
    )

    views = models.PositiveIntegerField(
        verbose_name="views",
        default=0,
        editable=False,
    )

    author_ip = models.GenericIPAddressField(
        verbose_name="author IP",
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
        # Remove leading slashes from `local_path`
        self.local_path = self.local_path.lstrip("/")

        # Check `local_path` for some common values we don't want to allow
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

        # Generate `title` from `local_path` if it's not provided
        if not self.title:
            self.title = deslugify(self.local_path)

        return super().clean()

    def get_absolute_url(self) -> str:
        """Return redirect URL."""
        from django.urls import reverse

        return reverse("redirects:redirect", kwargs={"local_path": self.local_path})

    @property
    def absolute_path(self) -> str:
        """Return absolute fake URL path."""
        if not self.local_path.startswith("/"):
            return f"/{self.local_path}"

        return self.local_path

    def increase_view_count(self) -> None:
        """Increase redirect view count by 1."""
        self.views += 1
        self.save()

    def get_fakester_links(self, request: HttpRequest | None = None) -> list[str]:
        """Return fakester redirect links for all available domains."""
        urls = []

        scheme = request.scheme if request and request.scheme else "http"

        if request:
            # The domain currently browsed by the user should always be shown first
            url = URL.build(
                scheme=scheme,
                host=request.get_host(),
                path=self.absolute_path,
            )
            urls.append(str(url))

        if settings.AVAILABLE_DOMAINS:
            for domain in settings.AVAILABLE_DOMAINS:
                url = URL.build(scheme=scheme, host=domain, path=self.absolute_path)

                # Avoid duplicating the currently browsed domain
                if str(url) not in urls:
                    urls.append(str(url))

        return urls
