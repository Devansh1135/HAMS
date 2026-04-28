from rest_framework import serializers
from .models import Appointment
from rest_framework.exceptions import ValidationError
from datetime import date


class AppointmentListCreateSerializer(serializers.ModelSerializer):
    day = serializers.DateField(input_formats=["%d-%m-%Y"],format='%d-%m-%Y')
    patient = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Appointment
        fields = "__all__"
        validators = []

    def validate_day(self, day):
        if day < date.today():
            raise ValidationError({"error": "appointment should be made in the future"})
        return day

    def validate(self, data):
        patient = self.context['request'].user.patient_profile
        day = data['day']
        time_slot = data['time_slot']
        doctor = data['doctor']
        if Appointment.objects.filter(patient = patient,day=day, time_slot=time_slot).exists():
            raise ValidationError('You already have an appointment in this slot.')
        if Appointment.objects.filter(doctor = doctor, day=day, time_slot=time_slot).exists():
            raise ValidationError('This doctor already has an appointment in that slot.')
        return super().validate(data)

class AppointmentRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
