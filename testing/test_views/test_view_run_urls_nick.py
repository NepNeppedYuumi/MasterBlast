# Third-party imports
from django.contrib.auth.models import User
from django.test import Client
import pytest


@pytest.mark.django_db
def test_login_page():
    """Test login url.
    Test if page works for login when you go to the login url.
    """
    client = Client()

    response = client.get("/login")

    assert 'pages/login.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_signup_page():
    """Test signup url.
    Test if page works for signup when you go to the signup url.
    """
    client = Client()

    response = client.get("/signup")

    assert 'pages/signup.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_perosnalia_page():
    """Test personalia url.
    Tests if url goes to login with next personalia if a user tries to go to
    the personalia page when the user is not logged in.
    Then tries to go to the personalia when the user is logged in, wich 
    should go to personalia.
    """
    client = Client()

    response = client.get("/personalia")

    assert response.url == '/login?next=/personalia'

    user = User.objects.create(username='testuser_personalia_ut')
    user.set_password('12345')
    user.save()

    client.login(username='testuser_personalia_ut', password='12345')
    response = client.get("/personalia")

    assert 'pages/personalia.html' in [template.name for template in response.templates]
