from django.urls import path
from . import views
urlpatterns = [
    path('',views.AppointmentListCreateView.as_view(), name = 'list-add-appointment')
]