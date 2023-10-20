"""Module contains routing definitions."""

from __future__ import annotations

from django.urls import path

from products import views

urlpatterns = [
    path(
        "categories/<int:product_category_id>/products",
        views.ProductCategoryDetailView.as_view(),
    ),
]
