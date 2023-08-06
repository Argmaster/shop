"""Module contains routing definitions."""

from __future__ import annotations

from django.urls import path

from transactions import views

urlpatterns = [
    path("", views.index, name="index"),
]
