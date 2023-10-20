"""Module contains routing definitions."""

from __future__ import annotations

from django.urls import path

from products import views

urlpatterns = [
    path("<int:product_id>/", views.make_transaction, name="index"),
]
