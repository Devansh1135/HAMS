from rest_framework import serializers
from .models import PatientProfile
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
            "sex",
            "age",
            "weight",
            "username",
            "password",
            "email",
            "role",
            "phone",
        ]

    def create(self, validated_data):
        # pop fields for profile
        sex = validated_data.pop("sex")
        print(sex)
        age = validated_data.pop("age")
        weight = validated_data.pop("weight")

        # creating User object
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # creating Patient Profile
        PatientProfile.objects.create(user=user, sex=sex, weight=weight, age=age)
        return user
