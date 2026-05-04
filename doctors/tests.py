from django.test import TestCase
import pytest
from django.urls import reverse
from common.models import Role
# Create your tests here.

# @pytest.mark.django_db
# def test_add_doctor(create_user, create_doctor, api_client):
#     user = create_user(username = "Doctor1", email = "doctor1@gmail.com", password = "Doctor@1", role = Role.objects.create(name="doctor"))
#     create_doctor(user=user, firstname="Stephen", lastname="Strange", sex="male", specialty="Sorcery", degree="MBBS")

@pytest.mark.django_db
def test_add_doctor(api_client, create_user):
    user = create_user(username = "admin", email = "admin@admin.com", password = "Admin@1", role = Role.objects.create(name="admin"), is_staff = True)
    Role.objects.create(name = "doctor")
    data = {
        "username": "Doctor1",
        "password" : "Doctor@1",
        "email" : "Doctor1@example.com",
        "sex" : "M",
        "firstname" : "Stephen",
        "lastname" : "Strange", 
        "specialty": "Sorcery",
        "degree": "MD",
        "role" : "doctor"
}
    api_client.force_authenticate(user=user)
    url = reverse('doctors-list-create')
    response = api_client.post(url,data)
    assert response.status_code == 201
    assert response.data["email"] == "Doctor1@example.com"
    assert response.data["username"] == "Doctor1"

@pytest.mark.django_db
def test_list_doctors(api_client, create_doctor, create_user):
    user = create_user(username = "Doctor", email = "Doctor1@gmail.com", password = "Doctor@1", role = Role.objects.create(name="doctor"))
    create_doctor(user=user, firstname="Stephen", lastname="Strange", sex="male", specialty="Sorcery", degree="MBBS")
    url = reverse('doctors-list-create')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["count"] > 0

@pytest.mark.django_db
def test_retrieve_doctor(api_client, create_doctor, create_user):
    user = create_user(username = "Doctor", email = "Doctor1@gmail.com", password = "Doctor@1", role = Role.objects.create(name="doctor"))
    doctor = create_doctor(user=user, firstname="Stephen", lastname="Strange", sex="male", specialty="Sorcery", degree="MBBS")
    api_client.force_authenticate(user=user)
    url = reverse("doctor-profile", kwargs = {'pk' : doctor.id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["firstname"] == "Stephen"
    assert response.data["user"]["username"] == "Doctor"