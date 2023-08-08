"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

from transactions.models import Product

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def make_transaction(request: HttpRequest, product_id: int) -> HttpResponse:
    """Return index page of local orders application."""
    product = Product.objects.get(pk=product_id)
    return render(
        request,
        "farm/transaction.django-html",
        {
            "product": product,
        },
    )
