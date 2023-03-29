# Generated by Django 4.1.7 on 2023-03-29 12:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Redirect",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="modified at"),
                ),
                (
                    "local_path",
                    models.CharField(
                        error_messages={"unique": "This path is already taken."},
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Allowed characters: a-z, A-Z, 0-9, slash (/), dot (.), underscore (_) and hyphen (-).",
                                regex="^[a-zA-Z0-9/._-]+$",
                            )
                        ],
                        verbose_name="local path",
                    ),
                ),
                ("destination_url", models.URLField(verbose_name="destination URL")),
                (
                    "views",
                    models.PositiveIntegerField(
                        default=0, editable=False, verbose_name="views"
                    ),
                ),
                (
                    "author_ip",
                    models.GenericIPAddressField(
                        editable=False, null=True, verbose_name="author IP"
                    ),
                ),
            ],
            options={
                "verbose_name": "redirect",
                "verbose_name_plural": "redirects",
            },
        ),
    ]
