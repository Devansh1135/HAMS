from django.contrib import admin
from .models import DoctorAvailibility, DoctorProfile
# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(DoctorAvailibility)