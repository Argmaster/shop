"""Models used by products database."""

from __future__ import annotations

from django.db import models


def make_price_field() -> models.Field:
    """Create price field object with predefined constraints."""
    return models.DecimalField(max_digits=10, decimal_places=4)


def make_description_field(length: int | None = None) -> models.Field:
    """Create description field."""
    return models.TextField(max_length=length, default="", blank=True)


class QuantityUnit(models.Model):
    """Represents unit which can be used to specify amount of items in transaction."""

    display_name = models.CharField(max_length=100)
    """Name of unit visible for user in GUI."""

    description = make_description_field(500)
    """Description of unit visible for user in GUI."""

    def __str__(self) -> str:
        return self.display_name


class Currency(models.Model):
    """Represents currency which can be used to express value of items."""

    display_name = models.CharField(max_length=100)
    """Name of currency, visible for user in GUI."""

    description = make_description_field(500)
    """Description of currency, visible for user in GUI."""

    class Meta:
        """Model metadata."""

        verbose_name_plural = "Currencies"

    def __str__(self) -> str:
        return self.display_name


class ProductCategory(models.Model):
    """Model representing a group (category) of products."""

    display_name = models.CharField(max_length=100)
    """Product name, visible for user in GUI"""

    description = models.TextField(max_length=None, default="", blank=True)
    """Product description, visible for user in GUI."""

    is_description_html = models.BooleanField(default=False)
    """Toggles rendering description content as html."""

    category_image_alt = models.TextField(max_length=None, default="", blank=True)
    """Alternative text for category image."""

    category_image = models.ImageField(
        upload_to="products/product_category/category_image/upload/",
        null=True,
        blank=True,
    )

    precedence_index = models.IntegerField(
        default=0,
        verbose_name="Index defining ordering of products",
    )
    """Index indicating product category ordering, categories with higher indexes will
    be presented before those with lowe indexes."""

    is_public_category = models.BooleanField(default=False)
    """Toggles visibility of product category to users."""

    class Meta:
        """Model metadata."""

        verbose_name_plural = "Product categories"

    def __str__(self) -> str:
        return self.display_name

    def get_all_available_products(self) -> models.QuerySet[Product]:
        """Get set of all available products."""
        return self.product_set.filter(is_product_public=True)


class Product(models.Model):
    """Model representing a product which can be sold."""

    product_code = models.CharField(max_length=50, unique=True)
    """Product code, visible for user in GUI."""

    display_name = models.CharField(max_length=100)
    """Product name, visible for user in GUI."""

    description = models.TextField(max_length=None, default="", blank=True)
    """Product description, visible for user in GUI."""

    is_description_html = models.BooleanField(default=False)
    """Toggles rendering description content as html."""

    is_product_public = models.BooleanField(default=False)
    """Toggle product visibility for customers."""

    precedence_index = models.IntegerField(
        default=0,
        verbose_name="Index defining ordering of products",
    )
    """Index indicating product ordering, products with higher indexes will be
    presented before those with lowe indexes."""

    categories = models.ManyToManyField(to=ProductCategory)
    """Categories this product is assigned to, preferably one, but can be many."""

    stock_in_quantity_units = models.PositiveIntegerField(default=0)
    """Product quantity, visible for user in GUI."""

    is_stock_public = models.BooleanField(default=False)
    """Toggle stock visibility for customers."""

    quantity_units = models.ForeignKey(
        QuantityUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    """Unit of quantity of product (<count> times 1 of <unit>, ie. 6x1KG)."""

    price_of_one_unit = make_price_field()
    """Price of 1 unit of this item."""

    price_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    """Currency used price."""

    is_price_public = models.BooleanField(default=False)
    """Toggle price visibility for customers."""

    is_ordering_enabled = models.BooleanField(default=False)
    """Control customers ability to order this product."""

    expected_delivery_time = models.TextField(default="3 tygodnie")
    """Expected delivery time in days"""

    def __str__(self) -> str:
        return self.display_name

    def unit_price_with_currency(self) -> str:
        """Get price of unit with currency as string."""
        c = self.price_currency
        return f"{self.price_of_one_unit:.2f} {c.display_name if c else ''}"

    @property
    def is_available_for_purchase(self) -> bool:
        """Return true if product is available for purchase."""
        return (
            self.is_ordering_enabled
            and self.is_product_public
            and ((not self.is_stock_public) or (self.stock_in_quantity_units > 0))
        )

    def get_first_image(self) -> ProductPhoto | None:
        """Return first related ProductPhoto object."""
        return (
            ProductPhoto.objects.filter(product=self)
            .order_by("precedence_index")
            .first()
        )


class ProductPhoto(models.Model):
    """Photo of a product."""

    name = models.CharField(max_length=100)
    """Product name, visible to user in web GUI."""

    alt = models.CharField(max_length=255)
    """Alternative text for image on web page."""

    precedence_index = models.IntegerField(
        default=0,
        verbose_name="Index defining ordering of products",
    )
    """Index indicating product photos ordering, photos with higher indexes will be
    presented before those with lowe indexes."""

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    """Product related to this image."""

    image = models.ImageField(
        upload_to="products/product_photo/image/upload/",
        null=True,
        blank=True,
    )
    """Actual image file."""

    def __str__(self) -> str:
        return super().__str__()


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
        QuantityUnit,
        on_delete=models.CASCADE,
    )
    """Unit used to designate quantity."""

    unit_price = make_price_field()
    """Price of 1 unit of this item."""

    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    """Currency used price."""

    def __str__(self) -> str:
        return (
            f"{self.product.display_name} ({self.unit_price}x{self.quantity} "
            f"{self.unit_of_quantity.display_name})"
        )
