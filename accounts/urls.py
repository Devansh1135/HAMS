from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("signup/", views.PatientSignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path(
        "password-change/", views.PasswordChangeView.as_view(), name="password change"
    ),
    path("me/", views.GetUserProfile.as_view(), name="get profile"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
