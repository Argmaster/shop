"""Module contains application config."""

from __future__ import annotations

from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """Application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "transactions"
