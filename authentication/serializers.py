from asyncio import events
from dataclasses import fields
from datetime import datetime
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import Device, SmsOTP, User, UserCardBilling
from events.models import Event, EventStatus
from events.serializers import EventSerializer
from general.models import Friends
from events.serializers import UniversitySerializer, UserUniversitySerializer
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from payments.models import EventTransaction

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
        events=Event.objects.filter(user_id=obj.id,archived=False).all()
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
        events=Event.objects.filter(user_id=obj.id,archived=False).all()
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

class UserDetailSerializer(serializers.ModelSerializer):
    university=UserUniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    friends_count=serializers.SerializerMethodField()
    user_score=serializers.SerializerMethodField()
    pinned_events=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','friends_count','user_score','profile_access_type','user_type','pinned_events')
    def get_event_count(self,obj):
        # eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        events=Event.objects.filter(user_id=obj.id,archived=False).all()
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
    def get_pinned_events(self,obj):
        eventIds=EventStatus.objects.filter(user_id=obj.id,pinned=True).values("event_id")
        events=Event.objects.filter(pk__in=eventIds)
        # serializer=EventSerializer(events,many=True)
        eventList=[]
        if events.count()>0:
            for event in events:
                serializer=EventSerializer(event)
                event=serializer.data        
                # guest user's details
                if len(event['guests'])>0:
                    guestUsers=[];
                    for guest in event['guests']:
                        user=User.objects.filter(id=guest).first()
                        if user is not None:
                            serializer=UserSerializer(user)
                            userItem={}
                            userItem=serializer.data
                            eventStatus=EventStatus.objects.filter(user_id=user.id).all()
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

                            userItem.update({"user_score":user_score})
                            guestUsers.append(userItem)

                        event['guests']=guestUsers
                        lint_score=0
                        eventStatus=EventStatus.objects.filter(event_id=event['id']).all()    
                        if eventStatus.count() > 0:
                            for eventStatusItem in eventStatus:
                                if eventStatusItem.checked_in:
                                    lint_score+=6
                                if eventStatusItem.pinned:
                                    lint_score+=5
                                if eventStatusItem.paid:
                                    lint_score+=4
                                if eventStatusItem.guest_list:
                                    lint_score+=3
                                if eventStatusItem.invited:
                                    lint_score+=2
                        #status list for current user
                        status_list={'checked_in':False,'pinned':False,'liked':False,'joined':False,'going':False,'not_going':False,'paid':False,'guest_list':False,'invited':False}
                        eventStatusByUser=EventStatus.objects.filter(user_id=obj.id,event_id=event['id']).first()    
                        if eventStatusByUser is not None:
                            if eventStatusByUser.checked_in:
                                status_list['checked_in']=True
                            if eventStatusByUser.pinned:
                                status_list['pinned']=True
                            if eventStatusByUser.liked:
                                status_list['liked']=True    
                            if eventStatusByUser.joined:
                                status_list['joined']=True
                            if eventStatusByUser.going:
                                status_list['going']=True
                            if eventStatusByUser.not_going:
                                status_list['not_going']=True                        
                            if eventStatusByUser.paid:
                                status_list['paid']=True
                                # transaction
                                eventTransactionByUser=EventTransaction.objects.filter(user_id=obj.id,event_id=event['id']).first()    
                                event["transaction_id"]=None
                                if eventTransactionByUser is not None:
                                    event["transaction_id"]=eventTransactionByUser.transaction_id
        
                            if eventStatusByUser.guest_list:
                                status_list['guest_list']=True
                            if eventStatusByUser.invited:
                                status_list['invited']=True 

                        
                        event['status_list']=status_list
                        event['lint_score']=lint_score
                        isLive=False
                        if datetime.strptime(event['event_end_date'],"%Y-%m-%d")  >= datetime.today() >= datetime.strptime(event['event_start_date'],"%Y-%m-%d"):
                            current_time = datetime.now().strftime('%H:%M:%S')
                            if event['event_start_time'] and event['event_end_time'] and is_between(current_time,(event['event_start_time'],event['event_end_time'])):
                                isLive=True
                        event['is_live']=isLive
                        eventList.append(event)
        return eventList

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
       return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]        