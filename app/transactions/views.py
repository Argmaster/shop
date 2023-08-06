"""Module contains definitions of http endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse

if TYPE_CHECKING:
    from django.http import HttpRequest


def index(_request: HttpRequest) -> HttpResponse:
    """Return index page of local orders application."""
    return HttpResponse("Hello, world. You're at the transactions index.")
