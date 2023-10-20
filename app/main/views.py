"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.shortcuts import render
from django.views import generic

from main.models import CarouselImage, SiteConfiguration
from products.models import ProductCategory

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class HomePageView(generic.View):
    """View onto available products."""

    template_name = "main/index.django-html"

    def get(
        self,
        request: HttpRequest,
        *_args: Any,
        **_kwargs: Any,
    ) -> HttpResponse:
        """Generate and return GET request response."""
        context: dict[str, Any] = {}

        context["all_carousel_images_list"] = CarouselImage.objects.filter(
            is_public=True,
        ).order_by("precedence_index")

        context["all_product_categories_list"] = ProductCategory.objects.filter(
            is_public_category=True,
        ).order_by("precedence_index")

        (context["site_configuration"]) = SiteConfiguration.load()

        return render(request, self.template_name, context)
