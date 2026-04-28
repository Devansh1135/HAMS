from rest_framework import serializers
from .models import DoctorProfile, User, DoctorAvailibility, BlockedSlot
from common.models import Role
from common.serializers import UserSerializer
import re
from rest_framework.exceptions import ValidationError


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

    def validate_password(self,password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
        if re.fullmatch(pattern,password):
            return password
        raise ValidationError({
            "message" : "Password must contain Atleast 1 Uppercase character , 1 lowercase character , 1 digit and 1 special character"
        })
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

class DoctorProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = DoctorProfile
        fields = "__all__"
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user',None)
        if user_data:
            user = UserSerializer(
                instance=instance.user,
                data=user_data,
                partial=True
            )
        return super().update(instance, validated_data)

class DoctorAvalibilityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailibility
        fields = '__all__'

class DoctorAvalibilityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailibility
        fields = '__all__'
        read_only_fields = ['doctor']
    

class AddBlockedSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedSlot
        fields = ['blocked_date', 'start_time', 'end_time']
    
