from django.db import models
from accounts.models import PatientProfile
from doctors.models import DoctorProfile
from  django.db.models import constraints
# Create your models here.

class Appointment(models.Model):
    status_choices = [
        ("booked", "Booked"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.PROTECT)
    status = models.CharField(choices=status_choices, max_length=10)
    day = models.DateField()
    time_slot = models.TimeField()
    created_at = models.DateTimeFieldTimeField(auto_now_add=True)

    class Meta:
        constraints = models.UniqueConstraint(fields=['doctor','day','time_slot'])
        