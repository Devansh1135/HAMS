from django.contrib import admin
from .models import User, PatientProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomuserChangeForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomuserChangeForm
    model = User


admin.site.register(User, CustomUserAdmin)
admin.site.register(PatientProfile)