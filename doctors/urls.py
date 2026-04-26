from django.urls import path
from . import views

urlpatterns = [
    path('',views.DoctorProfileListCreateView.as_view(), name = 'doctors list'),
    path('<int:pk>/', views.DoctorProfileRetrieveUpdateDeleteView.as_view(), name = 'doctor profile'),
    path('<int:pk>/availibility/', views.DoctorAvalibilityCreateRetrieveView.as_view(), name = 'doctor availibility'),
    path('<int:pk>/availibility/<int:avail_id>/', views.DoctorAvailibilityUpdateDestroyView.as_view(), name = 'doctor availibility'),
    path('<int:pk>/slots/', views.AvailableSlotsView.as_view(), name= 'doctor slots'),
    
]
