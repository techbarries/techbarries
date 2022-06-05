from dataclasses import fields
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import Device, SmsOTP, User
from events.models import EventStatus
from general.models import Friends
from events.serializers import UniversitySerializer
from django.db.models import Q

class PulseUserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    friends_count=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','friends_count','profile_access_type','user_type')
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    def get_event_count(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        return eventStatus.count()    
    def get_friends_count(self,obj):
        friends=Friends.objects.filter(Q(sent_to_user_id=obj.id )|Q(sent_by_user_id=obj.id),status=True).all()
        return friends.count()        
           
class UserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    friends_count=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','friends_count','profile_access_type','user_type')
    def get_event_count(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        return eventStatus.count()
    def get_friends_count(self,obj):
        friends=Friends.objects.filter(Q(sent_to_user_id=obj.id )|Q(sent_by_user_id=obj.id),status=True).all()
        return friends.count()        
 
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields='__all__'

class SmsOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=SmsOTP
        fields='__all__'
