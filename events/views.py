from unicodedata import name
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from events.models import University, Venue,Event
from rest_framework.response import Response
from events.serializers import EventSerializer, UniversitySerializer, VenueSerializer
from rest_framework import status

# Create your views here.

class CreateEventAPIView(CreateAPIView):
    serializer_class=EventSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Event created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
    # serializer_class=EventSerializer
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)   
    # def perform_create(self, serializer):
    #     return super().perform_create(serializer)
class EventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        events=Event.objects.filter(user_id=user_id).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            res={"status":True,"message":"events found","data":{"events":serializer.data}}
        else:
            res={"status":False,"message":"Not found","data":{}}
        return Response(res)
class UniversityListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        universities=University.objects.filter().values()
        if universities.count() > 0:
            serializer = UniversitySerializer(universities, many=True)
            res={"status":True,"message":"universities found","data":{"universities":serializer.data}}
        else:
            res={"status":False,"message":"Not found","data":{}}
        return Response(res)
    
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