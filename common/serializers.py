from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only = True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email']