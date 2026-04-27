from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Appointment
from .serializers import AppointmentListCreateSerializer
# Create your views here.

class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentListCreateSerializer
    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        id = user.id
        role = user.role.name
        if role == "patient":
            return Appointment.objects.filter(patient = id)
        elif role == "doctor":
            return Appointment.objects.filter(doctor = id)
        
        
