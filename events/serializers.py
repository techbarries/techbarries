from rest_framework import serializers
from events.models import Age, Dress, Event, EventImage, Food, Music, University, Venue, VenueImage

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields=['event','image']
        
class EventSerializer(serializers.ModelSerializer):
    event_images=EventImageSerializer(many=True,read_only=True)
    class Meta:
        model=Event
        fields='__all__'

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

                 