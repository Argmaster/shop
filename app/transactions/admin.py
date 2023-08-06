"""Add models to admin GUI."""
from __future__ import annotations

from django.contrib import admin

from transactions.models import Product, Transaction, TransactionItem, Unit

admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
