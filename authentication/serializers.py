from dataclasses import fields
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import Device, SmsOTP, User
from events.models import EventStatus
from events.serializers import UniversitySerializer

class PulseUserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','profile_access_type')
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    def get_event_count(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        return eventStatus.count()    
          
class UserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','profile_access_type')
    def get_event_count(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        return eventStatus.count()
 
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields='__all__'

class SmsOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=SmsOTP
        fields='__all__'
