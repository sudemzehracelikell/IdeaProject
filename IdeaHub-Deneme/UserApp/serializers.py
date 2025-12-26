from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userName', 'email', 'password', 'role']

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'