from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PatientSignupSerializer
from rest_framework.response import Response
from django.http import request
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken , BlacklistedToken
# Create your views here.

User = get_user_model()

class PatientSignupView(APIView):
    def post(self, request):
        serializer = PatientSignupSerializer(data = request.data)
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
            return Response({"error" : "Password is incorrect!!!!"}, status=400)
        user.set_password(new_password)
        user.save()
        tokens = OutstandingToken.objects.filter(user = user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response({"message" : "Password changed successfully!!!"})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        tokens = OutstandingToken.objects.filter(user = user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
         