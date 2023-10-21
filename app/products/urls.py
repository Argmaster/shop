"""Module contains routing definitions."""

from __future__ import annotations

from django.urls import path

from products import views

urlpatterns = [
    path(
        "categories/<int:pk>/",
        views.ProductCategoryView.as_view(),
    ),
    path(
        "categories/<int:category_pk>/product/<int:product_pk>/",
        views.ProductView.as_view(),
    ),
]
