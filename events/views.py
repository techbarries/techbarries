from unicodedata import name
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from events.models import University, Venue

from events.serializers import EventSerializer, UniversitySerializer, VenueSerializer

# Create your views here.

class CreateEventAPIView(CreateAPIView):
    serializer_class=EventSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class UniversityListAPIView(ListAPIView):
    serializer_class=UniversitySerializer
    
    def get_queryset(self):
        return University.objects.all()

class UniversityAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=UniversitySerializer
    lookup_field="id"
    queryset = University.objects.all()

class CreateUniversityAPIView(CreateAPIView):
    serializer_class=UniversitySerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class VenueListAPIView(ListAPIView):
    serializer_class=VenueSerializer
    
    def get_queryset(self):
        return Venue.objects.all()

class VenueAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=VenueSerializer
    lookup_field="id"     
    queryset = Venue.objects.all()

class CreateVenueAPIView(CreateAPIView):
    serializer_class=VenueSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)    