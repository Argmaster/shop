"""Models used by home page."""

from __future__ import annotations

from typing import Any

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

    precedence_index = models.IntegerField(
        default=0,
        verbose_name="Index defining precedence of this image.",
    )
    """Index defining precedence of this image in comparison to other images.
    Can be used to reorder images in carousel."""

    def __str__(self) -> str:
        return self.name


class SiteConfiguration(models.Model):
    """Singleton model for holding site configuration."""

    footer_copyright = models.CharField(
        max_length=100,
        default="© 2023 Makatawi",
        blank=True,
    )
    """Copyright string to be displayed in footer."""

    contact_phone_number = models.CharField(max_length=100, default="", blank=True)
    """Phone number to be displayed in contact field."""

    contact_email = models.CharField(max_length=255, default="", blank=True)
    """Email address to be displayed in contact field."""

    contact_facebook_url = models.CharField(max_length=1024, default="", blank=True)
    """Phone number to be displayed in contact field."""

    contact_instagram_url = models.CharField(max_length=1024, default="", blank=True)

    contact_youtube_url = models.CharField(max_length=1024, default="", blank=True)

    contact_address_for_correspondence = models.CharField(
        max_length=1500,
        default="",
        blank=True,
    )

    def __str__(self) -> str:
        return "SiteConfiguration"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save the current instance. Override this in a subclass if you want to control
        the saving process.

        The 'force_insert' and 'force_update' parameters can be used to insist that the
        "save" must be an SQL insert or update (or equivalent for non-SQL backends),
        respectively. Normally, they should not be set.
        """
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *_args: Any, **_kwargs: Any) -> tuple[int, dict[str, int]]:
        """Delete object from database, noop."""
        # Ensure row can't be deleted
        return 0, {}

    @staticmethod
    def load() -> SiteConfiguration:
        """Load singleton instance."""
        obj, created = SiteConfiguration.objects.get_or_create(pk=1)
        return obj
