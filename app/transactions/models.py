"""Models used by transactions database."""

from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models


class Unit(models.Model):
    """Represents unit which can be used to specify amount of items in transaction."""

    short_name = models.CharField(max_length=100, unique=True)

    long_name = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.short_name


class Currency(models.Model):
    """Represents currency which can be used to express value of items."""

    short_name = models.CharField(max_length=100, unique=True)

    long_name = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.short_name


class Product(models.Model):
    """Model representing a product which can be sold."""

    name = models.CharField(max_length=100)
    """Product name, visible in web GUI"""

    description = models.TextField()
    """Product description, visible in web GUI."""

    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    """Photo/icon of product."""

    stock_quantity = models.PositiveIntegerField(default=0)
    """Product quantity, partially visible in GUI."""

    is_stock_public = models.BooleanField(default=False)
    """Toggle stock visibility to customers."""

    unit_quantity = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    """Price of 1 unit of this item."""

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    """Model representing transaction with customer."""

    placed_date = models.DateTimeField(auto_now_add=True)
    """Date when transaction was started (order was placed by customer)."""

    expected_finalization_date = models.DateTimeField()
    """Date when transaction was expected to finalize."""

    finalization_date = models.DateTimeField()
    """Date when transactions was finalized."""

    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Transaction {self.pk}"


class TransactionItem(models.Model):
    """Item included in transaction."""

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    """Parent transaction."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    """Product exchanged in transaction."""

    quantity = models.PositiveIntegerField(default=1)
    """Quantity of items exchanged."""

    unit_of_quantity = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )
    """Unit used to designate quantity."""

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    """Price of 1 unit of this item."""

    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    """Currency used price."""

    def __str__(self) -> str:
        return (
            f"{self.product.name} ({self.unit_price}x{self.quantity} "
            f"{self.unit_of_quantity.short_name})"
        )
