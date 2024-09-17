from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def permission_denied_page(request: WSGIRequest, exception: str) \
    -> HttpResponse:
    return render(request, '403.html')