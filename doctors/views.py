from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import DoctorProfile, User, DoctorAvailibility, BlockedSlot
from .serializers import DoctorProfileSerializer, DoctorProfileRetrieveSerializer, DoctorAvalibilityCreateSerializer, DoctorAvalibilityUpdateSerializer, AddBlockedSlotSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import datetime
from doctors.services import SlotCalculationService

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
    
    
class DoctorAvalibilityCreateRetrieveView(generics.ListCreateAPIView):
    serializer_class = DoctorAvalibilityCreateSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]
    def get_queryset(self):
        return get_list_or_404(DoctorAvailibility, doctor = self.kwargs['pk'])
    
class DoctorAvailibilityUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorAvalibilityUpdateSerializer
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]
    def get_object(self):
        return get_object_or_404(DoctorAvailibility, doctor = self.kwargs['pk'], id = self.kwargs['avail_id'])
    
class AvailableSlotsView(generics.ListAPIView):
    permission_classes = [AllowAny] 
    def list(self, request, *args, **kwargs):
        print("=== DEBUG: View called ===")
        doctor_id = self.kwargs.get('pk')
        print(f"Doctor ID from URL: {doctor_id}, Type: {type(doctor_id)}")
        date_str = request.query_params.get('date')
        print(f"Date string from query params: {date_str}")
        if not date_str:
            return Response(
                {
                    "error" : "date parameter is required!!!!"
                }
            )
        try:
            appointment_date = datetime.strptime(date_str, '%d-%m-%Y').date()
        except ValueError:
            return Response({
                "error" : "Invalid date  format. enter date in DD-MM-YYYY format"
            })
        
        try:
            slots = SlotCalculationService.get_avalible_slots(doctor_id, appointment_date)
        except ValueError as e:
            return Response({
                "error" : str(e)
            })
        
        response_data = {
            "doctor_id" : doctor_id,
            "date" : appointment_date.strftime('%d-%m-%Y'),
            "available_slots" : slots,

        }

        return Response(response_data)
    

class AddBlockedSlot(generics.ListCreateAPIView):
    serializer_class = AddBlockedSlotSerializer
    def get_queryset(self):
        return BlockedSlot.objects.filter(doctor= self.kwargs['pk'])
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        doctor_id = self.kwargs['pk']
        doctor = get_object_or_404(DoctorProfile, id= doctor_id)
        print(type(doctor))
        serializer.save(doctor= doctor)

class UnblockSlot(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        slot_id = self.kwargs['slot_id']
        BlockedSlot.objects.get(id=slot_id).delete()
        return Response({
            "message" : "Slot succesfully unblocked"
        }, status=200)
    