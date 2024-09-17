# Third-party imports
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Local imports
from Blaster.models.BlastBuddies import BlastBuddies


def signup_page(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    """Renders the signup page

    If the signup button is clicked, the fields username email
    and password are obtained and the user is signed up and logged in.
    If there is an error the page reloads using redirect back to the
    signup page. If the signup was succesful the user will redirect to the index 
    page and a blastbuddie object will be made for that user to prevent
    errors of the object not existing  

    :param request: Django request object
    :type request: WSGIRequest
    :return: renders the signup page or redirects to the home page
    :rtype: HttpResponse | HttpResponseRedirect
    """
    if request.POST.get('Signup'):
        username = request.POST['Username']
        email = request.POST['Email']
        password = request.POST['Password'] 
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            login(request, user)
            BlastBuddies.objects.get_or_create(user=request.user)
            return redirect('/')
        except Exception as e:
            print(e) # prints the exeption for dev purposes
            return redirect(signup_page)
    return render(request, 'pages/signup.html')
