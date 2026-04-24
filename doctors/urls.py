from django.urls import path
from . import views

urlpatterns = [
    path('',views.DoctorProfileListCreateView.as_view(), name = 'doctors list'),
    path('<int:pk>/', views.DoctorProfileRetrieveUpdateDeleteView.as_view(), name = 'doctor profile'),
]
