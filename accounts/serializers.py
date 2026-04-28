from rest_framework import serializers
from .models import PatientProfile
from common.models import Role, UserRole
from common.serializers import UserSerializer
from django.contrib.auth import get_user_model
import re
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator


User = get_user_model()


class PatientSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    sex = serializers.CharField(write_only=True)
    DOB = serializers.DateField(write_only=True)
    weight = serializers.IntegerField(write_only=True, validators = [MinValueValidator(1)])

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "phone",
            "sex",
            "DOB",
            "weight",
            
        ]

    def validate_password(self,password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
        if re.fullmatch(pattern,password):
            return password
        raise ValidationError({
            "message" : "Password must contain Atleast 1 Uppercase character , 1 lowercase character , 1 digit and 1 special character"
        })
    

    def create(self, validated_data):
        # pop fields for profile
        sex = validated_data.pop("sex")
        print(sex)
        DOB = validated_data.pop("DOB")
        weight = validated_data.pop("weight")
        print(validated_data)
        # creating User object
        password = validated_data.pop("password")
        role_name = UserRole.PATIENT.value
        role = Role.objects.get(name=role_name)
        user = User(role=role, **validated_data)
        user.set_password(password)
        user.save()

        # creating Patient Profile
        PatientProfile.objects.create(user=user, sex=sex, weight=weight, DOB=DOB)
        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    class Meta:
        model = PatientProfile
        fields = '__all__'

