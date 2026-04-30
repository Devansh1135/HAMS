from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PatientSignupSerializer, PatientProfileSerializer
from rest_framework.response import Response
from django.http import request
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework import generics
from .models import PatientProfile
from common.paginators import BasePagination
from common.permissions import IsPatient

# Create your views here.

User = get_user_model()


class PatientSignupView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PatientSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        # confirm_password = request.data.get("confirm_password")
        # if new_password != confirm_password:
        #     return Response({"error" : "Confirm password does not match!!!!"}, status=400)
        if not user.check_password(old_password):
            return Response({"error": "Password is incorrect!!!!"}, status=400)
        user.set_password(new_password)
        user.save()
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response({"message": "Password changed successfully!!!"})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response(
            {"message": "Logged out successfully"},
            status=200
        )


class GetUserProfile(generics.RetrieveUpdateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

    def get_permissions(self):
        return [IsPatient()]

    def get_object(self):
        return PatientProfile.objects.get(user=self.request.user)
