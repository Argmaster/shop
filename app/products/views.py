"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from django.http import Http404
from django.views.generic import DetailView

from products.models import ProductCategory

if TYPE_CHECKING:
    from django.db.models import QuerySet


class ProductCategoryDetailView(DetailView):
    """Detail view for ProductCategory object."""

    model = ProductCategory
    template_name = "products/product.django-html"  # Specify your template path here
    context_object_name = "product_category"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Extend context data."""
        context = super().get_context_data(**kwargs)
        context["all_product_categories_list"] = ProductCategory.objects.all()
        return context

    def get_object(
        self,
        queryset: Optional[QuerySet[ProductCategory]] = None,
    ) -> ProductCategory:
        """Retrieve the object for this view."""
        obj: ProductCategory = super().get_object(queryset=queryset)
        if not obj.is_public_category:
            msg = "This category is not public."
            raise Http404(msg)
        return obj
