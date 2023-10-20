"""Add models to admin GUI."""
from __future__ import annotations

from typing import Any

from django.contrib import admin

from products.models import (
    Currency,
    CustomerInfo,
    Product,
    ProductCategory,
    ProductPhoto,
    QuantityUnit,
    Transaction,
    TransactionItem,
)


class QuantityUnitAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = ("display_name",)
    search_fields = ("display_name", "description")
    ordering = ("display_name",)


class CurrencyAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = ("display_name",)
    search_fields = ("display_name", "description")
    ordering = ("display_name",)


class ProductCategoryAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = (
        "display_name",
        "precedence_index",
        "count_of_items_in_category",
        "is_public_category",
    )
    list_filter = ("is_public_category",)
    search_fields = ("display_name", "description")
    list_editable = ("precedence_index", "is_public_category")
    ordering = ("precedence_index",)

    def count_of_items_in_category(self, obj: ProductCategory) -> int:
        """Return all products assigned to this category."""
        return obj.product_set.count()


class ProductPhotoInline(admin.StackedInline):
    """Inlined item creator menu."""

    model = ProductPhoto
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""

    list_display = (
        "product_code",
        "display_name",
        "is_product_public",
        "precedence_index",
        "category_names",
        "is_stock_public",
        "is_price_public",
        "is_ordering_enabled",
    )
    list_editable = (
        "is_product_public",
        "precedence_index",
        "is_stock_public",
        "is_price_public",
        "is_ordering_enabled",
    )  # For easier editing directly from the list view
    list_filter = (
        "is_stock_public",
        "is_price_public",
        "is_ordering_enabled",
        "categories",
    )
    search_fields = ("product_code", "display_name", "description")
    ordering = ("precedence_index",)

    inline = (ProductPhotoInline,)

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "product_code",
                    "display_name",
                    "description",
                    "is_product_public",
                    "precedence_index",
                    "categories",
                ),
            },
        ),
        (
            "Transaction details",
            {
                "fields": (
                    "stock_in_quantity_units",
                    "is_stock_public",
                    "quantity_units",
                    "price_of_one_unit",
                    "price_currency",
                    "is_price_public",
                    "is_ordering_enabled",
                    "expected_delivery_time",
                ),
            },
        ),
    )

    def category_names(self, product: Product) -> Any:
        """Get list of product categories."""
        return ", ".join(repr(c.display_name) for c in product.categories.all())


class ProductPhotoAdmin(admin.ModelAdmin):
    """Customized admin view onto model."""


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

    inlines = (TransactionItemInline,)


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
    list_filter = ("unit_of_quantity", "product__display_name")
    search_fields = ("transaction__id", "product__display_name")
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


admin.site.register(QuantityUnit, QuantityUnitAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(TransactionItem, TransactionItemAdmin)
