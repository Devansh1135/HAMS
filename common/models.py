from django.db import models
from enum import Enum
class Role(models.Model):
    ROLE_CHOICES = [
        ("patient","Patient"),
        ("doctor","Doctor")
    ]
    name = models.CharField(choices=ROLE_CHOICES,max_length=10)

    def __str__(self):
        return self.name
    

class UserRole(Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"