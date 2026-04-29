from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.db.models import constants

# Create your models here.


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    sex = models.CharField(choices=[("M", "male"), ("F", "female")], max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    specialty = models.CharField(max_length=20)
    degree = models.CharField(max_length=10)

    def clean(self):
        if self.user.role != "doctor":
            raise ValidationError("user must be a doctor!!!!")

    def __str__(self):
        return self.user.username


class DoctorAvailibility(models.Model):
    days = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="availability"
    )
    days_of_week = models.IntegerField(choices=days)
    time_in = models.TimeField()
    time_out = models.TimeField()
    slot_duration = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "days_of_week"], name="unique_availibility"
            )
        ]


class BlockedSlot(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="blocked_slots"
    )
    blocked_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
