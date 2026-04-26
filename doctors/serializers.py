from rest_framework import serializers
from .models import DoctorProfile, User, DoctorAvailibility
from common.models import Role
from common.serializers import UserSerializer


class DoctorProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    sex = serializers.CharField(write_only=True)
    specialty = serializers.CharField(write_only=True)
    degree = serializers.CharField(write_only=True)
    firstname = serializers.CharField(write_only=True)
    lastname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "phone",
            "firstname",
            "lastname",
            "sex",
            "specialty",
            "degree",
        ]

    def to_representation(self, instance):
    # Handle both User and DoctorProfile instances
        if isinstance(instance, DoctorProfile):
            user = instance.user
            return {
                "email": user.email,
                "phone": user.phone,
                "firstname": instance.firstname,
                "lastname": instance.lastname,
                "sex": instance.sex,
                "specialty": instance.specialty,
                "degree": instance.degree,
            }
        return super().to_representation(instance)


    def create(self, validated_data):
        firstname = validated_data.pop("firstname")
        lastname = validated_data.pop("lastname")
        sex = validated_data.pop("sex")
        specialty = validated_data.pop("specialty")
        degree = validated_data.pop("degree")
        password = validated_data.pop("password")

        role = Role.objects.get(name="doctor")
        user = User(role=role, **validated_data)
        user.set_password(password)
        user.save()
        DoctorProfile.objects.create(
            user=user,
            firstname=firstname,
            lastname=lastname,
            sex=sex,
            specialty=specialty,
            degree=degree,
        )
        return user

class DoctorProfileRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = DoctorProfile
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        phone = validated_data.pop('phone', None)
        instance = super().update(instance, validated_data)
        user = instance.user
        if username:
            user.username = username
        if email:
            user.email = email
        if phone:
            user.phone = phone
        user.save()
        return instance

class DoctorAvalibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailibility
        fields = '__all__'
    
    

    