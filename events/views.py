from datetime import date, datetime
from unicodedata import name
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from authentication.models import User
from events.models import EventImage, EventStatus, University, Venue,Event
from rest_framework.response import Response
from events.serializers import EventSerializer, UniversitySerializer, VenueSerializer
from rest_framework import status
from rest_framework.views import APIView


# Create your views here.

class CreateEventAPIView(CreateAPIView):
    serializer_class=EventSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Event created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            if request.FILES.getlist('event_images[]') is not None:
                event_images=request.FILES.getlist('event_images[]')
                for image in event_images:
                    eventImage=EventImage.objects.create(event=Event.objects.get(id=serializer.data['id']),image=image)
                    eventImage.save()
            res.update(data=serializer.data)
            # create event status
            EventStatus.objects.create(event_id=Event.objects.get(id=serializer.data['id']),user_id= User.objects.get(id=serializer.data['user_id']) ,hosted=True)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
    # serializer_class=EventSerializer
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)   
    # def perform_create(self, serializer):
    #     return super().perform_create(serializer)

class EventStatusAPIView(APIView):
    def get(self,request,event_id,user_id,status):
        status_list = ["checked_in","checked_out","pinned","un_pinned"]
        if status in status_list:
            eventStatus=EventStatus.objects.filter(user_id=user_id,event_id=event_id).first()
            if eventStatus is not None:
                if status == "checked_in":
                    eventStatus.checked_in=True
                if status == "checked_out":
                    eventStatus.checked_in=False
                if status == "pinned":
                    eventStatus.pinned=True
                if status == "un_pinned":
                    eventStatus.pinned=False
                eventStatus.save();    
                res={"status":True,"message":"event status updated successfully","data":{}}
                return Response(res)
            else:
                if status == "checked_in":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id),checked_in=True)
                if status == "checked_out":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id),checked_in=False)
                if status == "pinned":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,pinned=True)
                if status == "un_pinned":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id),pinned=False)
                res={"status":True,"message":"event status created successfully","data":{}}
                return Response(res)
        else:
            res={"status":False,"message":"Invalid status provided.","data":{'status_list':status_list}}
            return Response(res)


        
        
class EventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        events=Event.objects.filter(user_id=user_id).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            events_list=[]
            for event in serializer.data:
                eventStatus=EventStatus.objects.filter(event_id=event['id']).all()
                lint_score=0
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

                event['lint_score']=lint_score
                isLive=False
                if str(event['event_end_date']) == str(date.today()):
                    current_time = datetime.now().strftime('%H:%M:%S')
                    if event['event_start_time'] and event['event_end_time'] and is_between(current_time,(event['event_start_time'],event['event_end_time'])):
                        isLive=True
                event['is_live']=isLive
                events_list.append(event)
            res={"status":True,"message":"events found","data":{"events":events_list}}
        else:
            res={"status":False,"message":"Not found","data":{}}
        return Response(res)

class PastEventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        events=Event.objects.filter(user_id=user_id,event_end_date__lte=datetime.today()).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            res={"status":True,"message":"events found","data":{"events":serializer.data}}
        else:
            res={"status":False,"message":"Not found","data":{}}
        return Response(res)
class UpcomingEventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        events=Event.objects.filter(user_id=user_id,event_end_date__gte=datetime.today()).all()
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


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
       return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]        