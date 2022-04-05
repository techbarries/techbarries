from dataclasses import fields
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import Device, User

class PulseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','uid','user_token','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','country','university','email')
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
          
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','uid','user_token','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','country','university','email')

 
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields='__all__'           