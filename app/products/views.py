"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import Any

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from main.models import SiteConfiguration
from products.models import Product, ProductCategory


class ProductCategoryView(generic.View):
    """View onto available products."""

    template_name = "products/product_category.django-html"

    def get(
        self,
        request: HttpRequest,
        *_args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Generate and return GET request response."""
        context: dict[str, Any] = {}

        context["all_product_categories_list"] = ProductCategory.objects.filter(
            is_public_category=True,
        ).order_by("precedence_index")

        context["site_configuration"] = SiteConfiguration.load()

        obj = get_object_or_404(ProductCategory, pk=kwargs.get("pk"))

        if not obj.is_public_category:
            raise Http404

        context["product_category"] = obj
        context["product_category_all_products"] = obj.get_all_available_products()

        return render(request, self.template_name, context)


class ProductView(generic.View):
    """View onto available products."""

    template_name = "products/product.django-html"

    def get(
        self,
        request: HttpRequest,
        *_args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Generate and return GET request response."""
        context: dict[str, Any] = {}

        context["all_product_categories_list"] = ProductCategory.objects.filter(
            is_public_category=True,
        ).order_by("precedence_index")

        context["site_configuration"] = SiteConfiguration.load()

        category = get_object_or_404(ProductCategory, pk=kwargs.get("category_pk"))
        if not category.is_public_category:
            raise Http404

        product = get_object_or_404(
            Product,
            pk=kwargs.get("product_pk"),
            categories=category,
        )
        if not product.is_product_public:
            raise Http404

        context["product_category"] = category
        context["product"] = product

        return render(request, self.template_name, context)
