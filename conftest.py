import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from accounts.models import PatientProfile
from doctors.models import DoctorProfile, DoctorAvailibility

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()



@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        password = kwargs.pop('password')
        user = User.objects.create_user(**kwargs)
        user.set_password(password)
        user.save()
        return user
    return make_user

@pytest.fixture
def create_patient():
    def make_patient(**kwargs):
        user = kwargs.pop('user')
        sex = kwargs.pop('sex')
        weight = kwargs.pop('weight')
        DOB = kwargs.pop('DOB')
        profile = PatientProfile.objects.create(user = user , sex = sex , weight = weight, DOB = DOB)
        return profile
    return make_patient

@pytest.fixture
def create_doctor():
    def make_doctor(**kwargs):
        user = kwargs.pop('user')
        firstname = kwargs.pop('firstname')
        lastname = kwargs.pop('lastname')
        sex = kwargs.pop('sex')
        specialty = kwargs.pop('specialty')
        degree = kwargs.pop('degree')
        profile = DoctorProfile.objects.create(user=user, sex=sex, firstname=firstname, lastname=lastname, specialty=specialty, degree=degree)
        return profile
    return make_doctor