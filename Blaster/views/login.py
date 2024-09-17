# Third-party imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.handlers.wsgi import WSGIRequest


def login_page(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    """ renders login page

    If the signin button is clicked the fields username email
    and password are obtained then the user gets logged in, and 
    redirected to the index page.
    if the user login information is not correct, then a error
    message will be raised and the page reloaded using redirect,
    and thus the user will stay on the page. 

    :param WSGIRequest request: Django request object
    :return HttpResponse: login page
    :return redirect: redirects back to login page after a failure
    """
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        try:
            user = authenticate(request, username = username,
                                password = password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or "/"
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password')
        except PermissionDenied:
            messages.error(request, 'Permission denied to log in')
        except ValidationError as e:
            messages.error(request, f'Validation error: {e}')
        return redirect(login_page)
    return render(request, 'pages/login.html')


def logout_view(request: WSGIRequest) -> redirect:
    """ logs out user

    logs out the logged in user and redirects to the home page

    :param request: Django request object
    :type request: WSGIRequest
    :return: redirects back to login page after failure
    :rtype: redirect
    """
    logout(request)
    return redirect('/')
