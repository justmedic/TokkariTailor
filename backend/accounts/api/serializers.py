from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password', 'password2']
    
    def validate_email(self, value):
        lower_email = value.lower()
        if CustomUser.objects.filter(email=lower_email).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован.")
        return lower_email
    
    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Этот телефон уже зарегестрирован")
        return value
    

    def validate(self, value):
        if 'password' in value and 'password2' in value:
            if value['password'] != value['password2']:
                raise serializers.ValidationError({"password2": "Пароли не совпадают."})
        else:
            raise serializers.ValidationError("Требуется указать оба пароля.")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            
            username = validated_data.get('email').lower(),
            email=validated_data.get('email').lower(),
            phone=validated_data.get('phone'),
            password=validated_data.get('password')
        
        )
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is None:
            raise serializers.ValidationError("Invalid username/password.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        return {'user': user}
