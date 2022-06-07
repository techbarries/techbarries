from rest_framework import serializers
from authentication.models import User
from events.models import Age, Dress, Event, EventImage, EventStatus, Food, MenuImage, Music, RequestVenue, University, Venue, VenueImage
from django.db.models import Q
from general.models import Friends

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
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','friends_count','profile_access_type','user_type')
    def get_event_count(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        return eventStatus.count()    
    def get_friends_count(self,obj):
        friends=Friends.objects.filter(Q(sent_to_user_id=obj.id )|Q(sent_by_user_id=obj.id),status=True).all()
        return friends.count()                
class EventSerializer(serializers.ModelSerializer):
    event_images=EventImageSerializer(many=True,read_only=True)
    like_count=serializers.SerializerMethodField()
    joined_count=serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
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
        fields='__all__'

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
        return 75000
    def get_is_open(self,obj):
        return True
    def get_available_slots(self,obj):
        return "8pm-2pm"
    def get_price_range(self,obj):
        return "$25k-50k"                                                     

class RequestVenueSerializer(serializers.ModelSerializer): 
        class Meta:
            model=RequestVenue
            fields='__all__'                