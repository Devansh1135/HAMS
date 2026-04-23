from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    role = models.CharField(
        choices=[("patient", "Patient"), ("doctor", "Doctor"), ("admin", "Admin")],
        max_length=10,
        default="patient",
    )
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(("email address"), unique = True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    sex = models.CharField(choices=[("male", "M"), ("female", "F")], max_length=10)
    weight = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()

    def __str__(self):
        return self.user.username
