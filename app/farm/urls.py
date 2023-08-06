"""Module contains routing definitions."""

from __future__ import annotations

from django.urls import path

from farm import views

urlpatterns = [
    path("fruits/", views.index, name="index"),
]
