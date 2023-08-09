"""Models used by farm database."""

from __future__ import annotations

from django.db import models


def make_description_field(length: int | None = None) -> models.Field:
    """Create description field."""
    return models.TextField(max_length=length, default="", blank=True)


class CarouselImage(models.Model):
    """Database entry representing carousel image."""

    name = models.CharField(max_length=100, unique=True)

    description = make_description_field(500)

    change_interval_ms = models.PositiveIntegerField(
        default=5000,
        verbose_name="Change time (milliseconds).",
    )
    """Image change interval in milliseconds. After <change_interval_ms> milliseconds
    image will switch to next image in carousel."""

    image = models.ImageField(
        upload_to="main/carousel/images/",
        null=True,
        blank=True,
    )
    """Image object."""

    is_public = models.BooleanField(default=False)
    """Make image visible to customer."""

    index = models.IntegerField(
        default=0,
        verbose_name="Index defining precedence of this image.",
    )
    """Index defining precedence of this image in comparison to other images.
    Can be used to reorder images in carousel."""

    def __str__(self) -> str:
        return self.name
