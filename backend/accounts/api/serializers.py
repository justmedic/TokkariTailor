from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'password2']
        
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
