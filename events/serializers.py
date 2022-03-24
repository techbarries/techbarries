from rest_framework import serializers
from events.models import Event, University, Venue

class EventSerializer(serializers.ModelSerializer):
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