"""Add models to admin GUI."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.contrib import admin

from transactions.models import (
    Currency,
    CustomerInfo,
    Product,
    Transaction,
    TransactionItem,
    Unit,
)

if TYPE_CHECKING:
    from django.contrib.admin.options import InlineModelAdmin


class UnitAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = ("short_name",)
    search_fields = ("short_name", "description")
    ordering = ("short_name",)


class CurrencyAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = ("short_name",)
    search_fields = ("short_name", "description")
    ordering = ("short_name",)


class ProductAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = (
        "name",
        "stock_quantity",
        "unit_price_with_currency",
        "is_stock_public",
        "is_public",
        "is_ordering_enabled",
        "index",
    )
    list_editable = (
        "stock_quantity",
        "is_stock_public",
        "is_public",
        "is_ordering_enabled",
        "index",
    )  # For easier editing directly from the list view
    list_filter = (
        "is_stock_public",
        "is_public",
        "is_ordering_enabled",
    )
    search_fields = ("name", "description")
    ordering = ("name",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "square_image",
                    "wide_image",
                    "stock_quantity",
                    "unit_quantity",
                    "unit_price",
                    "price_currency",
                    "is_stock_public",
                    "is_public",
                    "is_ordering_enabled",
                ),
            },
        ),
    )


class TransactionItemInline(admin.StackedInline):
    """Inlined item creator menu."""

    model = TransactionItem
    extra = 1


class TransactionAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = (
        "placed_date",
        "expected_finalization_date",
        "finalization_date",
        "customer",
    )
    list_filter = ("placed_date", "expected_finalization_date", "finalization_date")
    search_fields = (
        "customer__username",
        "customer__first_name",
        "customer__last_name",
    )
    date_hierarchy = "placed_date"
    ordering = ("-placed_date",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "expected_finalization_date",
                    "finalization_date",
                    "customer",
                ),
            },
        ),
    )

    inlines: ClassVar[list[type[InlineModelAdmin]]] = [TransactionItemInline]


class CustomerInfoAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = ("name", "surname", "phone_number", "email")
    search_fields = ("name", "surname", "phone_number", "email")
    ordering = ("name", "surname")


class TransactionItemAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = (
        "transaction",
        "product",
        "quantity",
        "unit_of_quantity",
        "unit_price",
    )
    list_filter = ("unit_of_quantity", "product__name")
    search_fields = ("transaction__id", "product__name")
    ordering = ("transaction", "product")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "transaction",
                    "product",
                    "quantity",
                    "unit_of_quantity",
                    "unit_price",
                ),
            },
        ),
    )


admin.site.register(Unit, UnitAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(TransactionItem, TransactionItemAdmin)
