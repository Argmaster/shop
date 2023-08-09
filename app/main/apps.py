"""Configuration of "main" app."""
from __future__ import annotations

from django.apps import AppConfig


class MainConfig(AppConfig):
    """Configuration of main app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
