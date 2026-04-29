from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from common.models import Role


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, **extra_fields):
        if not email:
            raise ValueError("Email is required!!")
        if role is None:
            raise ValueError("Role must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        admin_role = Role.objects.get(name="admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, admin_role, **extra_fields)


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    sex = models.CharField(choices=[("male", "M"), ("female", "F")], max_length=10)
    weight = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    DOB = models.DateField()

    def __str__(self):
        return self.user.username
