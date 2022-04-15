from rest_framework import serializers
from events.models import Event, EventImage, University, Venue

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
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Venue
        fields='__all__'         