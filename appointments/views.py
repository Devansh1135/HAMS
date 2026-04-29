from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Appointment
from .serializers import AppointmentListCreateSerializer, AppointmentRetrieveUpdateDeleteSerializer
from datetime import datetime
from common.permissions import IsDoctor
from django.shortcuts import get_object_or_404
from common.paginators import BasePagination
from .tasks import send_appointment_confirmation_mail
import time
# Create your views here.


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentListCreateSerializer
    pagination_class = BasePagination
    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        id = user.id
        role = user.role.name
        if role == "patient":
            print(role,id)
            return Appointment.objects.filter(patient=user.patient_profile)
        elif role == "doctor":
            return Appointment.objects.filter(doctor=user.doctor_profile)

    def perform_create(self, serializer):
        patient = self.request.user.patient_profile
        start = time.time()
        appointment = serializer.save(patient=patient)
        print("SAVE DONE:", time.time() - start)
        send_appointment_confirmation_mail.delay(appointment.id)
        print("TASK SENT:", time.time() - start)
        
class AppointmentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDoctor]
    serializer_class = AppointmentRetrieveUpdateDeleteSerializer
    permission_classes = [IsDoctor]
    queryset = Appointment.objects.all()

