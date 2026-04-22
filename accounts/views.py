from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PatientSignupSerializer
from rest_framework.response import Response
# Create your views here.

class PatientSignupView(APIView):
    def post(self, request):
        serializer = PatientSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)