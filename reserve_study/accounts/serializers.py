from rest_framework import serializers
from .models import CustomUser,CommunityInfo
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
class CommunityInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CommunityInfo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class AccessUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccessUser
#         fields = '__all__'
        
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'phone_no', 'company', 'position', 'additional_info', 'role', 'is_active', 'is_superuser']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class UpdateSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_no', 'company', 'position', 'additional_info', 'role', 'is_active', 'is_superuser']

class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return data
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        