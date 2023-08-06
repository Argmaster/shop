from __future__ import annotations

from django.apps import AppConfig


class FarmConfig(AppConfig):
    """Farm web application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "farm"
