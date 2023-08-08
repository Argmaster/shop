"""Implements command which populates database with sample data."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from transactions.models import Currency, Product, Unit


class Command(BaseCommand):
    """Development helper command."""

    help = "Populates the database with sample data."  # noqa: A003

    def handle(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        """Handle command."""
        # Creating Units
        kg, created = Unit.objects.get_or_create(
            short_name="skrzynka (3KG)",
            description="Trzykilogramowa skrzynka.",
        )
        litr, created = Unit.objects.get_or_create(
            short_name="słoik (1L)",
            description="Litrowy słoik.",
        )

        # Creating Currency
        pln, created = Currency.objects.get_or_create(
            short_name="PLN",
            description="Polski Złoty",
        )

        # Creating Sample Products
        Product.objects.get_or_create(
            name="Borówka Amerykańska",
            description="Fresh Blueberries",
            stock_quantity=100,
            is_stock_public=True,
            unit_quantity=kg,
            unit_price=10.50,
            price_currency=pln,
            is_public=True,
            is_ordering_enabled=True,
        )

        Product.objects.get_or_create(
            name="Malina",
            description="Fresh Raspberries",
            stock_quantity=75,
            is_stock_public=True,
            unit_quantity=kg,
            unit_price=12.00,
            price_currency=pln,
            is_public=True,
            is_ordering_enabled=True,
        )

        Product.objects.get_or_create(
            name="Miód",
            description="Natural Honey",
            stock_quantity=50,
            is_stock_public=True,
            unit_quantity=litr,
            unit_price=30.00,
            price_currency=pln,
            is_public=True,
            is_ordering_enabled=True,
        )

        self.stdout.write(self.style.SUCCESS("Successfully populated sample data."))
