"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Return index page of local orders application."""
    return render(request, "farm/index.html")
