"""Implements command which populates database with sample data."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from main.models import SiteConfiguration
from products.models import (
    Currency,
    Product,
    ProductCategory,
    ProductPhoto,
    QuantityUnit,
)


class Command(BaseCommand):
    """Development helper command."""

    help = "Populates the database with sample data."  # noqa: A003

    def handle(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        """Handle command."""
        SiteConfiguration.objects.get_or_create(
            footer_copyright="© 2023 Makatawi",
            contact_phone_number="",
            contact_email="",
            contact_facebook_url="https://www.facebook.com/groups/529535354742862",
            contact_instagram_url="",
            contact_youtube_url="",
        )

        # Creating Units
        items, created = QuantityUnit.objects.get_or_create(
            display_name="szt.",
            description="sztuk",
        )
        # Creating Currency
        pln, created = Currency.objects.get_or_create(
            display_name="PLN",
            description="Polski Złoty",
        )

        lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

        # Creating Sample Products
        kom, created = ProductCategory.objects.get_or_create(
            display_name="Pamiątki komunijne",
            description=lorem,
            is_public_category=True,
        )

        ok, created = ProductCategory.objects.get_or_create(
            display_name="Pamiątki Okolicznościowe",
            description=lorem,
            is_public_category=True,
        )

        pas, created = ProductCategory.objects.get_or_create(
            display_name="Pamiątki pasowania na ucznia",
            description=lorem,
            is_public_category=True,
        )

        ab, created = ProductCategory.objects.get_or_create(
            display_name="Pamiątki dla abiturientów",
            description=lorem,
            is_public_category=False,
        )

        for cat, cat_name in zip(
            (kom, ok, pas, ab),
            ("kom", "ok", "pas", "ab"),
            strict=True,
        ):
            for i in range(20):
                product, created = Product.objects.get_or_create(
                    product_code=f"{cat_name}-{i}",
                    display_name=f"Product {cat_name} {i}",
                    description=lorem,
                    is_product_public=bool(i % 2),
                    precedence_index=i,
                    stock_in_quantity_units=1,
                    is_stock_public=False,
                    quantity_units=items,
                    price_of_one_unit=50.0,
                    price_currency=pln,
                    is_price_public=bool(i % 3),
                    is_ordering_enabled=bool(i % 4),
                    expected_delivery_time=f"{i} dni",
                )
                product: Product
                product.categories.set((cat,))

                for j in range(4):
                    ProductPhoto.objects.get_or_create(
                        name=f"{product.display_name} {j}",
                        alt=f"alt {product.display_name} {j}",
                        precedence_index=j,
                        product=product,
                    )

        self.stdout.write(self.style.SUCCESS("Successfully populated sample data."))
