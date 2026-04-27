from rest_framework import serializers
from .models import PatientProfile
from common.models import Role
from common.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    sex = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)
    weight = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "phone",
            "sex",
            "age",
            "weight",
            
        ]

    def create(self, validated_data):
        # pop fields for profile
        sex = validated_data.pop("sex")
        print(sex)
        age = validated_data.pop("age")
        weight = validated_data.pop("weight")
        print(validated_data)
        # creating User object
        password = validated_data.pop("password")
        role = Role.objects.get(name='patient')
        user = User(role=role, **validated_data)
        user.set_password(password)
        user.save()

        # creating Patient Profile
        PatientProfile.objects.create(user=user, sex=sex, weight=weight, age=age)
        return user

class PatientProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    class Meta:
        model = PatientProfile
        fields = '__all__'

