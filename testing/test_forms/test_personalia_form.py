# Third-party imports
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.test import Client
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_change_password():
    """Test password change.
    Tests if changing the password works on the personalia page.
    Checks if the user stays on the personalia page after changing the 
    password,
    and checks if the password is then the new password.
    After that it checks it again if it now stays the same if the old 
    password is incorect.
    """
    username = 'testuser_change_pw'
    password = '12345'
    new_password = '54321'
    user = User.objects.create_user(username=username, password=password)

    client = Client()
    client.login(username=username, password=password)

    response = client.post(reverse('personalia_page'), {
        'Old_Password': password,
        'New_Password': new_password,
        'New_Password2': new_password
    })

    assert response.url == '/personalia'

    user.refresh_from_db()
    assert user.check_password('54321') == True
    
    response = client.post(reverse('personalia_page'), {
        'Old_Password': password,
        'New_Password': 1,
        'New_Password2': 1
    })

    assert response.url == '/personalia'

    user.refresh_from_db()
    assert user.check_password('54321') == True


@pytest.mark.django_db
def test_search_user():
    """Test searching for user.
    Test if when you search for a new buddie, that the function finds 
    and returns the user in its json response.
    Then it tests if the user doesnt exist that it gives an empty json 
    response.
    """
    username = 'testuser_search'
    password = '12345'
    user = User.objects.create_user(username=username, password=password)
    user = User.objects.create_user(username='admin', password='admin')

    client = Client()
    client.login(username=username, password=password)
    response = client.get(reverse('search_user'), {'name': 'admin'})

    assert isinstance(response, JsonResponse)
    data = response.json()
    # test if works with existing username
    assert any(user['username'] == 'admin' for user in data['users'])

    response = client.get(reverse('search_user'), {'name': 'none_exits'})

    assert isinstance(response, JsonResponse)
    data = response.json()
    # test with name that doesnt exist
    assert data == {'users': []}
