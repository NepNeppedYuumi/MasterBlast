# Third-party imports
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_signup_form():
    """Test signup redirect.
    Tests if when the wrong signup is used that the user stays on the 
    signup page. The wrong user is a user this function makes and then
    trys to signup as, but that account already exist so there is no 
    correct signup.
    """
    username = 'testuser_signupd'
    email = 'no@reply.nl'
    password = '12345abC!'

    client = Client()

    data = {
        'Username': username,
        'Email': email,
        'Password': password
    }

    user = User.objects.create_user(username = username, password = password)

    response = client.post(reverse('signup'), data)

    assert 'pages/signup.html' in [template.name for template in response.templates]
