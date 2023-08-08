"""Module contains routing definitions."""

from __future__ import annotations

from django.urls import path

from farm import views

urlpatterns = [
    path("<int:product_id>/transaction/", views.make_transaction, name="index"),
]
