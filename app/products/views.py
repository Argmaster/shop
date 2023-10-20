"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import render

from products.models import Product

if TYPE_CHECKING:
    from django.http import HttpRequest


def index(_request: HttpRequest) -> HttpResponse:
    """Return index page of local orders application."""
    return HttpResponse("Hello, world. You're at the products index.")


def make_transaction(request: HttpRequest, product_id: int) -> HttpResponse:
    """Return index page of local orders application."""
    product = Product.objects.get(pk=product_id)
    return render(
        request,
        "products/product.django-html",
        {
            "product": product,
        },
    )
