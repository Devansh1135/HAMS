from django.test import TestCase
import pytest
from django.urls import reverse
from common.models import Role
# Create your tests here.

@pytest.mark.django_db
def test_signup(api_client):
    url = reverse('signup')
    Role.objects.create(name = "patient")
    data = {
        "username" : "Devansh4",
        "password" : "Devansh@4",
        "email" : "devanshjagatiya1135@gmail.com",
        "sex" : "M",
        "DOB" : "2005-03-11",
        "weight" : 80,
        "role" : "patient"
        
    }

    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["email"] == "devanshjagatiya1135@gmail.com"

@pytest.mark.django_db
def test_login(api_client, create_user):
    create_user(username = "Devansh4", email = "devanshjagatiya1135@gmail.com", password = "Devansh@4", role = Role.objects.create(name="patient"))
    url = reverse('login')
    data = {
        "password" : "Devansh@4",
        "email" : "devanshjagatiya1135@gmail.com"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    
    


@pytest.mark.django_db
def test_get_profile(create_user,api_client, create_patient):
    user = create_user(username = "Devansh4", email = "devanshjagatiya1135@gmail.com", password = "Devansh@4", role = Role.objects.create(name="patient"))
    create_patient(sex="male", weight = 80, user = user, DOB = "2005-03-11")
    url = reverse('get-profile')
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["user"]["username"] == "Devansh4"
    assert response.data["DOB"] == "2005-03-11"
    assert response.data["weight"] == 80

@pytest.mark.django_db
def test_update_patient(create_user,api_client, create_patient):
    user = create_user(username = "Devansh4", email = "devanshjagatiya1135@gmail.com", password = "Devansh@4", role = Role.objects.create(name="patient"))
    create_patient(sex="male", weight = 80, user = user, DOB = "2005-03-11")
    url = reverse('get-profile')
    api_client.force_authenticate(user=user)
    data = {
        "sex" : "female",
        "DOB" : "2005-03-11",
        "weight" : 65
    }
    response = api_client.put(url,data)
    assert response.status_code == 200
    assert response.data["weight"] == 65
    assert response.data["sex"] == "female"
