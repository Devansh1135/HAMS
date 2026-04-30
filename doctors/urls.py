from django.urls import path
from . import views

urlpatterns = [
    path("", views.DoctorProfileListCreateView.as_view(), name="doctors list"),
    path("me/", views.DoctorProfileUpdateView.as_view(), name="update-doctor"),
    path(
        "<int:pk>/",
        views.DoctorProfileRetrieveDeleteView.as_view(),
        name="doctor profile",
    ),
    path('me/availibility/', views.DoctorAvailibilityCreateView.as_view(),name = "add-avalibility"),
    path(
        "<int:pk>/availibility/",
        views.DoctorAvalibilityListView.as_view(),
        name="list-availibility",
    ),
    path(
        "<int:pk>/availibility/<int:avail_id>/",
        views.DoctorAvailibilityUpdateDestroyView.as_view(),
        name="doctor availibility",
    ),
    path("<int:pk>/slots/", views.AvailableSlotsView.as_view(), name="doctor slots"),
    path(
        "<int:pk>/blocked/", views.AddBlockedSlot.as_view(), name="block doctor slots"
    ),
    path(
        "<int:pk>/blocked/<int:slot_id>/",
        views.UnblockSlot.as_view(),
        name="unblock doctor slots",
    ),
]
