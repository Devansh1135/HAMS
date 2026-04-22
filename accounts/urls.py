from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.PatientSignupView.as_view(), name = 'signup'),
]