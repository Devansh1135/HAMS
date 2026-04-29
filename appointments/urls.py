from django.urls import path
from . import views

urlpatterns = [
    path("", views.AppointmentListCreateView.as_view(), name="list-add-appointment"),
    path(
        "<int:pk>/",
        views.AppointmentRetrieveUpdateDeleteView.as_view(),
        name="retrieve-update-delete-appointment",
    ),
]
