from rest_framework import serializers
from authentication.models import User
from events.models import Age, Dress, Event, EventImage, EventStatus, Food, Music, University, Venue, VenueImage

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields=['event','image']
class UserUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model=University
        fields='__all__'
class EventUserSerializer(serializers.ModelSerializer):
    university=UserUniversitySerializer(read_only=True)
    event_count=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','uid','user_token','username','first_name','last_name','profile_picture_url','profile_picture_image','is_active','phone_number','date_of_birth','job_title','degree_title','country','university','email','event_count','profile_access_type')
    def get_event_count(self,obj):
        eventStatus=EventStatus.objects.filter(user_id=obj.id,hosted=True)
        return eventStatus.count()        
class EventSerializer(serializers.ModelSerializer):
    event_images=EventImageSerializer(many=True,read_only=True)
    like_count=serializers.SerializerMethodField()
    user=serializers.SerializerMethodField()
    class Meta:
        model=Event
        fields='__all__'
    def get_like_count(self,obj):
        eventLikeStatus=EventStatus.objects.filter(event_id=obj.id,liked=True)
        return eventLikeStatus.count()    
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
        fields=['venue','image']
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
    dresses=DressSerializer(many=True,read_only=True)
    foods=FoodSerializer(many=True,read_only=True)
    musics=MusicSerializer(many=True,read_only=True)
    ages=AgeSerializer(many=True,read_only=True)
    event_count=serializers.SerializerMethodField()
    class Meta:
        model=Venue
        fields='__all__'

    def get_event_count(self,obj):
        eventStatus=Event.objects.filter(venue=obj.id)
        return eventStatus.count()    

                 