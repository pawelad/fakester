"""
Django models related utils.
"""
from django.db import models


class BaseModel(models.Model):
    """Base Django model with shared fields."""

    created_at = models.DateTimeField(
        verbose_name="created at",
        auto_now_add=True,
    )

    modified_at = models.DateTimeField(
        verbose_name="modified at",
        auto_now=True,
    )

    class Meta:
        abstract = True
