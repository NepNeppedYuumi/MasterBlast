from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def server_error_page(request: WSGIRequest) -> HttpResponse:
    return render(request, '500.html')