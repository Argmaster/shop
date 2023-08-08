"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import generic

from transactions.models import Product

if TYPE_CHECKING:
    from django.db.models import QuerySet


class ShopIndexView(generic.ListView):
    """View onto available products."""

    template_name = "shop/index.django-html"
    context_object_name = "item_list"

    def get_queryset(self) -> QuerySet[Product]:
        """Return the last five published questions."""
        return Product.objects.filter(is_public=True)
