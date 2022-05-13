from dataclasses import fields
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import Device, SmsOTP, User
from events.serializers import UniversitySerializer

class PulseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','uid','user_token','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','country','university','email')
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
          
class UserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    class Meta:
        model=User
        fields=('id','uid','user_token','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','country','university','email')

 
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields='__all__'

class SmsOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=SmsOTP
        fields='__all__'
