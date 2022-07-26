from rest_framework import serializers
from authentication.models import User
from events.models import Age, Dress, Event, EventImage, EventStatus, Food, MenuImage, Music, RequestVenue, University, Venue, VenueImage
from django.db.models import Q
from general.models import Friends
from datetime import datetime

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields=['id','event','image']
class UserUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model=University
        fields='__all__'
class EventUserSerializer(serializers.ModelSerializer):
    university=UserUniversitySerializer(read_only=True)
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


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model=University
        fields='__all__'

class VenueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueImage
        fields=['id','venue','image']
        
class VenueMenuImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuImage
        fields=['id','venue','image']        
class DressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dress
        fields=['pk','dress_name']
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields=['pk','food_name']
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields=['pk','music_name']
class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields=['pk','age_name']                                  
class VenueSerializer(serializers.ModelSerializer):
    venue_images=VenueImageSerializer(many=True,read_only=True)
    venue_menu_images=VenueMenuImageSerializer(many=True,read_only=True)
    dresses=DressSerializer(many=True,read_only=True)
    foods=FoodSerializer(many=True,read_only=True)
    musics=MusicSerializer(many=True,read_only=True)
    ages=AgeSerializer(many=True,read_only=True)
    event_count=serializers.SerializerMethodField()
    address=serializers.SerializerMethodField()
    latitude=serializers.SerializerMethodField()
    longitude=serializers.SerializerMethodField()
    total_users_joined=serializers.SerializerMethodField()
    is_open=serializers.SerializerMethodField()
    available_slots=serializers.SerializerMethodField()
    price_range=serializers.SerializerMethodField()
    promoter_user=EventUserSerializer(read_only=True)
    created_by=EventUserSerializer(read_only=True)
    class Meta:
        model=Venue
        # fields='__all__'
        exclude=('monday','monday_start_time','monday_end_time','tuesday','tuesday_start_time','tuesday_end_time','wednesday','wednesday_start_time','wednesday_end_time','thursday','thursday_start_time','thursday_end_time','friday','friday_start_time','friday_end_time','saturday','saturday_start_time','saturday_end_time','sunday','sunday_start_time','sunday_end_time','created_at','updated_at','archived')

    def get_event_count(self,obj):
        eventStatus=Event.objects.filter(venue=obj.id)
        return eventStatus.count()
    def get_address(self,obj):
        if obj.location is not None:
            return obj.location.place
    def get_latitude(self,obj):
        if obj.location is not None:
            return obj.location.latitude        
    def get_longitude(self,obj):
        if obj.location is not None:
            return obj.location.longitude 
    def get_total_users_joined(self,obj):
        events=Event.objects.values_list('id',flat=True).filter(venue=obj.id,archived=False).all()
        usersJoined=0
        if events.count()>0:
            eventStatus=EventStatus.objects.filter((Q(event_id__in=set(events))),joined=True).all()
            usersJoined=eventStatus.count()

        return usersJoined
    def get_is_open(self,obj):
        now = datetime.now()
        dayName=now.strftime("%A").lower()
        current_time =str( datetime.now().strftime('%H:%M:%S'))
        isOpen=False
        startTime=str( getattr(obj,dayName+"_start_time"))
        endTime=str( getattr(obj,dayName+"_end_time"))
        if getattr(obj,dayName) and startTime and endTime:
            if endTime < startTime:
                return current_time >= startTime or current_time <= endTime
            return startTime <= current_time <= endTime 
        return isOpen
    def get_available_slots(self,obj):
        now = datetime.now()
        dayName=now.strftime("%A").lower()
        startTime=getattr(obj,dayName+"_start_time")
        endTime=getattr(obj,dayName+"_end_time")
        return str(startTime.strftime("%I:%M") ) +"-"+str(endTime.strftime("%I:%M")) 
    def get_price_range(self,obj):
        return obj.price_details                                                     

class EventSerializer(serializers.ModelSerializer):
    event_images=EventImageSerializer(many=True,read_only=True)
    like_count=serializers.SerializerMethodField()
    joined_count=serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
    venue=serializers.SerializerMethodField()
    event_start=serializers.SerializerMethodField()
    event_end=serializers.SerializerMethodField()
    class Meta:
        model=Event
        fields='__all__'
    def get_like_count(self,obj):
        eventLikeStatus=EventStatus.objects.filter(event_id=obj.id,liked=True)
        return eventLikeStatus.count()    
    def get_joined_count(self,obj):
        eventJoinedStatus=EventStatus.objects.filter(event_id=obj.id,joined=True)
        return eventJoinedStatus.count()            
    def get_user(self,obj):
        serializer=EventUserSerializer(obj.user_id)
        return serializer.data
    def get_venue(self,obj):
        venue=None
        if obj.venue is not None:
            venueObj=Venue.objects.filter(id=obj.venue.id).first()
            if venueObj is not None:
                serializer=VenueSerializer(venueObj)
                venue=serializer.data
        return venue
    def get_event_end(self,obj):
        formated=None
        if obj.event_end_date and  obj.event_end_time is not None:
            formated=obj.event_end_time.strftime("%I:%M %p")+", "+obj.event_end_date.strftime("%a %d %b, %Y")
        return formated  
    def get_event_start(self,obj):
        formated=None
        if obj.event_start_date and  obj.event_start_time is not None:
            formated=obj.event_start_time.strftime("%I:%M %p")+", "+obj.event_start_date.strftime("%a %d %b, %Y")
        return formated
class RequestVenueSerializer(serializers.ModelSerializer): 
        class Meta:
            model=RequestVenue
            fields='__all__'                