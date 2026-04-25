from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import DoctorProfile, User
from .serializers import DoctorProfileSerializer, DoctorProfileRetrieveSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
# Create your views here.

class DoctorProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorProfileSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        doctors = DoctorProfile.objects.all()
        return doctors

    def perform_create(self, serializer):
        serializer.save()

class DoctorProfileRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileRetrieveSerializer
   
    def perform_destroy(self, instance):
        instance.user.delete()
        
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAdminUser()]
    
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"message" : "Doctor succesfully deleted"}, status=204)
    
    
    