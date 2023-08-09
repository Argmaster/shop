"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.views import generic

from main.models import CarouselImage
from transactions.models import Product

if TYPE_CHECKING:
    from django.db.models import QuerySet


class WithCarouselViewMixin:
    """Mixin for views which use `carousel.django-html` template."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get template context data."""
        context = {}
        context.update(super().get_context_data(**kwargs))  # type: ignore[misc]
        context.update(self.get_carousel_context())
        return context

    def get_carousel_context(self) -> dict[str, Any]:
        """Return carousel context."""
        return {
            "carousel_images": CarouselImage.objects.filter(is_public=True).order_by(
                "index",
            ),
        }


class ShopIndexView(WithCarouselViewMixin, generic.ListView):
    """View onto available products."""

    template_name = "main/index.django-html"
    context_object_name = "item_list"

    def get_queryset(self) -> QuerySet[Product]:
        """Return the last five published questions."""
        return Product.objects.filter(is_public=True).order_by("index")
