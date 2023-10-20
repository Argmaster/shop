"""Models used by products database."""

from __future__ import annotations

from django.db import models


def make_price_field() -> models.Field:
    """Create price field object with predefined constraints."""
    return models.DecimalField(max_digits=10, decimal_places=4)


def make_description_field(length: int | None = None) -> models.Field:
    """Create description field."""
    return models.TextField(max_length=length, default="", blank=True)


class Unit(models.Model):
    """Represents unit which can be used to specify amount of items in transaction."""

    short_name = models.CharField(max_length=100, unique=True)

    description = make_description_field(500)

    def __str__(self) -> str:
        return self.short_name


class Currency(models.Model):
    """Represents currency which can be used to express value of items."""

    short_name = models.CharField(max_length=100, unique=True)

    description = make_description_field(500)

    def __str__(self) -> str:
        return self.short_name


class Product(models.Model):
    """Model representing a product which can be sold."""

    name = models.CharField(max_length=100)
    """Product name, visible in web GUI"""

    description = make_description_field()
    """Product description, visible in web GUI."""

    square_image = models.ImageField(
        upload_to="product/square_image/",
        null=True,
        blank=True,
    )
    """Square image of product."""

    wide_image = models.ImageField(
        upload_to="product/wide_image/",
        null=True,
        blank=True,
    )
    """Wide image of product."""

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
    """Quantity of items expressed as volume of product in specified unit.
    (<count> times 1 of <unit>, ie. 6x1KG)."""

    unit_price = make_price_field()
    """Price of 1 unit of this item."""

    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    """Currency used price."""

    is_public = models.BooleanField(default=False)
    """Make product visible to customer."""

    is_ordering_enabled = models.BooleanField(default=False)
    """Control customers ability to order this product."""

    index = models.IntegerField(
        default=0,
        verbose_name="Index defining ordering of products",
    )
    """Index defining product ordering."""

    def __str__(self) -> str:
        return self.name

    def unit_price_with_currency(self) -> str:
        """Get price of unit with currency as string."""
        return f"{self.unit_price:.2f} {self.price_currency.short_name}"

    @property
    def is_available_for_purchase(self) -> bool:
        """Return true if product is available for purchase."""
        return self.is_ordering_enabled and self.is_public and self.stock_quantity > 0


class CustomerInfo(models.Model):
    """Information about customer."""

    name = models.TextField()
    """Customers name, always available."""

    surname = models.TextField(blank=True)
    """Customers name, sometimes available."""

    phone_number = models.TextField()
    """Customers phone number, always available."""

    email = models.EmailField()
    """Customers email address, always available."""

    def __str__(self) -> str:
        return f"{self.name} {self.surname} ({self.phone_number})"


class Transaction(models.Model):
    """Model representing transaction with customer."""

    placed_date = models.DateTimeField(auto_now_add=True)
    """Date when transaction was started (order was placed by customer)."""

    expected_finalization_date = models.DateTimeField()
    """Date when transaction was expected to finalize."""

    finalization_date = models.DateTimeField()
    """Date when products was finalized."""

    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    """Reference to customer info."""

    comment = make_description_field()
    """Comment added by customer"""

    is_finalized = models.BooleanField(default=False)
    """Boolean indicator of transaction finalization."""

    def __str__(self) -> str:
        return f"Transaction {self.pk}"


class TransactionItem(models.Model):
    """Item included in transaction."""

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    """Parent transaction."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    """Product exchanged in transaction."""

    quantity = models.PositiveIntegerField(default=0)
    """Quantity of items exchanged."""

    unit_of_quantity = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )
    """Unit used to designate quantity."""

    unit_price = make_price_field()
    """Price of 1 unit of this item."""

    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    """Currency used price."""

    def __str__(self) -> str:
        return (
            f"{self.product.name} ({self.unit_price}x{self.quantity} "
            f"{self.unit_of_quantity.short_name})"
        )
