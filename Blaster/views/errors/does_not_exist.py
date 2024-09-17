from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def does_not_exist_page(request: WSGIRequest, exception: str) -> HttpResponse:
    return render(request, '404.html')