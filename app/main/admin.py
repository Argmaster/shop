"""Add models to admin GUI."""
from __future__ import annotations

from django.contrib import admin

from main.models import CarouselImage, SiteConfiguration


class CarouselImageAdmin(admin.ModelAdmin):
    """Django admin view config."""

    list_display = ("name", "change_interval_ms", "is_public", "precedence_index")
    list_filter = ("is_public",)
    search_fields = ("name", "description")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "change_interval_ms",
                    "image",
                    "is_public",
                    "precedence_index",
                ),
            },
        ),
    )
    ordering = (
        "precedence_index",
    )  # To display images based on their index by default
    readonly_fields = ("image",)
    list_editable = (
        "is_public",
        "precedence_index",
    )  # For easier editing directly from the list view


admin.site.register(CarouselImage, CarouselImageAdmin)
admin.site.register(SiteConfiguration)
