from dataclasses import fields
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import Device, SmsOTP, User, UserCardBilling
from events.models import Event, EventStatus
from general.models import Friends
from events.serializers import UniversitySerializer
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class PulseUserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    friends_count=serializers.SerializerMethodField()
    user_score=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','friends_count','user_score','profile_access_type','user_type')
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    def get_event_count(self,obj):
        # eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        events=Event.objects.filter(user_id=obj.id).all()
        return events.count()    
    def get_friends_count(self,obj):
        friends=Friends.objects.filter(Q(sent_to_user_id=obj.id )|Q(sent_by_user_id=obj.id),status=True).all()
        return friends.count()        
    def get_user_score(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id).all()
        user_score=0
        if eventStatus.count() > 0:
            for eventStatusItem in eventStatus:
                if eventStatusItem.hosted:
                    user_score+=7
                if eventStatusItem.checked_in:
                    user_score+=6
                if eventStatusItem.pinned:
                    user_score+=5
                if eventStatusItem.paid:
                    user_score+=4
                if eventStatusItem.guest_list:
                    user_score+=3
                if eventStatusItem.invited:
                    user_score+=2
                if eventStatusItem.public:
                    user_score+=1
                if eventStatusItem.not_going:
                    user_score+=0
        return user_score              
class UserSerializer(serializers.ModelSerializer):
    university=UniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    friends_count=serializers.SerializerMethodField()
    user_score=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','friends_count','user_score','profile_access_type','user_type')
    def get_event_count(self,obj):
        # eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        events=Event.objects.filter(user_id=obj.id).all()
        return events.count()
    def get_friends_count(self,obj):
        friends=Friends.objects.filter(Q(sent_to_user_id=obj.id )|Q(sent_by_user_id=obj.id),status=True).all()
        return friends.count() 
    def get_user_score(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id).all()
        user_score=0
        if eventStatus.count() > 0:
            for eventStatusItem in eventStatus:
                if eventStatusItem.hosted:
                    user_score+=7
                if eventStatusItem.checked_in:
                    user_score+=6
                if eventStatusItem.pinned:
                    user_score+=5
                if eventStatusItem.paid:
                    user_score+=4
                if eventStatusItem.guest_list:
                    user_score+=3
                if eventStatusItem.invited:
                    user_score+=2
                if eventStatusItem.public:
                    user_score+=1
                if eventStatusItem.not_going:
                    user_score+=0
        return user_score                
 
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user_id', 'fcm_token'),
                message=_("The device already exists for current user.")
            )
        ]
        fields='__all__'
class UserCardBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserCardBilling
        fields='__all__'
        
class SmsOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=SmsOTP
        fields='__all__'
