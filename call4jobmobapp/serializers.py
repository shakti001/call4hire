from rest_framework import serializers
from call4jobapp.models import *

from django.contrib.auth.hashers import make_password

class RegitserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "email", "password", "roll", "username", "office_address", "employee_address", "country_code", "phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

    # if 'roll' == 'homenowner':
    #     def create(self, validated_data):
    #         user = User(email = validated_data['email'], roll = validated_data['roll'], mobile_number = validated_data['mobile_number'], first_name=validated_data['first_name'], last_name=validated_data['last_name'], profile_pic=validated_data['profile_pic'])
    #         user.set_password(validated_data['password'])
    #         user.save()
    #         return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

