from rest_framework import serializers
from call4jobapp.models import *

from django.contrib.auth.hashers import make_password

class RegitserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    gender = serializers.CharField()
    
    username = serializers.CharField()
    
    dob = serializers.DateTimeField()
    
    office_address = serializers.CharField()
    
    home_address = serializers.CharField()
    
    country_code = serializers.CharField()
    
    phone_number = serializers.CharField()
    
    login_source = serializers.CharField()
    
    

    class Meta:
        model = User
        fields = [ "email", "password","gender", "username", "dob","office_address", "home_address", "country_code", "phone_number", "login_source"]
        extra_kwargs = {"password": {"write_only": True}}



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    fcm_token = serializers.CharField()
    login_source = serializers.CharField()
    
 