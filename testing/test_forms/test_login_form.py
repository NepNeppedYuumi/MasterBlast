# Third-party imports
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_login_form():
    """Test user log in.
    Tests if the user can login in and then goes to the correct pages
    after login.
    Checks when user logs in correctly if the url went to index page.
    Then checks when user logs in with wrong information(doest log in) 
    taht the user stays on the login page.
    """
    username = 'testuser_login'
    password = '12345'
    user = User.objects.create_user(username = username, password = password)

    client = Client()

    data = {
        'Username': username,
        'Password': password
    }

    response = client.post(reverse('login'), data)

    assert response.url == '/'

    data['Password'] = 'fout'
    response = client.post(reverse('login'), data)

    assert response.url == '/login'
