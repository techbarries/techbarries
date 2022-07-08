import ast
from datetime import date, datetime
from unicodedata import name
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from authentication.models import Device, User
from authentication.serializers import DeviceSerializer, UserSerializer
from events.models import EventImage, EventStatus, University, Venue,Event, VenueImage, VenueStatus
from rest_framework.response import Response
from events.serializers import EventSerializer, RequestVenueSerializer, UniversitySerializer, VenueSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from fcm import Fcm

from general.models import Notification
from payments.models import EventTransaction

# Create your views here.

class CreateEventAPIView(CreateAPIView):
    serializer_class=EventSerializer
    def post(self,request):
        try:
            request.data['user_id']
        except KeyError:
            res={"status":False,"message":"user_id missing","data":{}}
            return Response(res,status=status.HTTP_200_OK)        
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
            # invite guests
            guests=serializer.data['guests']
            date=serializer.data['event_start_date']
            if date:
                cDate=datetime.strptime(date,'%Y-%m-%d')
                date=cDate.strftime('%A, %B %d, %Y')
            for guest in guests:
                EventStatus.objects.create(event_id=Event.objects.get(id=serializer.data['id']),user_id= User.objects.get(id=guest) ,invited=True)
                #notification
                user=User.objects.filter(pk=serializer.data['user_id']).first()
                if user is not None:
                    serializer_user=UserSerializer(user)
                    desc="You have been invited to the event '"+serializer.data['name']+"' on "+date+" by @"+serializer_user.data['first_name']
                    details={"has_button":True,"button_count":2,"positive_button":"Accept","negative_button":"Decline","type":"EVENT_INVITE","id":serializer.data['id'],"desc":"","action":None}
                    Notification.objects.create(title="You got invitation!",description=desc,redirect_to="EVENT_PAGE",details=details,user_id=User.objects.get(id=guest),created_by=user)
                    
                    sentToUserDevices=Device.objects.filter(user_id=guest).all()
                    if sentToUserDevices.count()>0:
                        device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                        for device in device_serializer.data:
                            if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                                fcm=Fcm()
                                fcm.send(device['fcm_token'],"You got invitation!",desc,{"redirect_to":"EVENT_PAGE"})
    
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
    def put(self,request):
        try:
            request.data['id']
        except KeyError:
            res={"status":False,"message":"Id missing","data":{}}
            return Response(res,status=status.HTTP_200_OK)  
        event=Event.objects.filter(pk=request.data['id']).first()
        if event is None:
            res={"status":False,"message":"Event not found","data":{}}
            return Response(res)
        serializer=self.serializer_class(event,data=request.data)
        res={"status":True,"message":"Event updated successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            if request.FILES.getlist('event_images[]') is not None:
                event_images=request.FILES.getlist('event_images[]')
                for image in event_images:
                    eventImage=EventImage.objects.create(event=Event.objects.get(id=serializer.data['id']),image=image)
                    eventImage.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)        
        
    # serializer_class=EventSerializer
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)   
    # def perform_create(self, serializer):
    #     return super().perform_create(serializer)
class EventImageDeleteAPIView(APIView):
    def delete(self,request,id, *args, **kwargs):
         image=EventImage.objects.filter(id=id).first()
         if image is not None:
            image.delete()
            res={"status":True,"message":"Event Image deleted successfully","data":{}}
         else:
            res={"status":False,"message":"Event Image not found","data":{}}
         return Response(res,status=status.HTTP_200_OK) 
        
class EventDetailAPIView(APIView):
    def get(self,request,event_id,user_id):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        event=Event.objects.filter(id=event_id).first()
        if event is None:
            res={"status":False,"message":"Event not found","data":{}}
            return Response(res)
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
                eventStatusByUser=EventStatus.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                        eventTransactionByUser=EventTransaction.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                res={"status":True,"message":"event found","data":{"event":event}}
                return Response(res)
class EventStatusAPIView(APIView):
    """Following are possible values for the status types
    \n"checked_in","checked_out","pinned","un_pinned","paid","joined","going","not_going","liked","un_liked",leave"
    """
    def get(self,request,event_id,user_id,status):
        status_list = ["checked_in","checked_out","pinned","un_pinned","liked","un_liked","paid","joined","going","not_going"]
        if status in status_list:
            if status=='joined':
                event=Event.objects.filter(id=event_id).first()
                if event is not None:
                    serializer=EventSerializer(event)
                    if serializer.data['joined_count']>=serializer.data['open_guests_list']:
                        res={"status":False,"message":"Can't join.Open guests list full","data":{}}
                        return Response(res)
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
                if status == "liked":
                    eventStatus.liked=True
                if status == "un_liked":
                    eventStatus.liked=False 
                if status == "joined":
                    eventStatus.joined=True 
                if status == "paid":
                    eventStatus.paid=True                       
                if status == "going":
                    eventStatus.going=True 
                    eventStatus.not_going=False
                if status == "not_going":
                    eventStatus.going=False 
                    eventStatus.joined=False
                    eventStatus.not_going=True                                                                              
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
                if status == "liked":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,liked=True)
                if status == "joined":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,joined=True)
                if status == "paid":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,paid=True)
                if status == "going":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,going=True,not_going=False)
                if status == "not_going":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,going=False,joined=False,not_going=True)            
                if status == "un_liked":
                    EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id),liked=False)    
                res={"status":True,"message":"event status created successfully","data":{}}
                return Response(res)
        elif status=='leave':
            eventStatus=EventStatus.objects.filter(user_id=user_id,event_id=event_id).first()
            if eventStatus is not None:
                eventStatus.delete()
                res={"status":True,"message":"Left from event successfully","data":{}}
            else:
                res={"status":False,"message":"Event status not found.","data":{}}
            return Response(res)
        else:
            res={"status":False,"message":"Invalid status provided.","data":{'status_list':status_list}}
            return Response(res)

class EventShareAPIView(APIView):
     """Required data
     {
    "event_id":1,
    "user_id":1,
    "to_user_id":[
        1,
        2,
        3
    ]
}
     """
     def post(self,request):
        try:
            request.data['event_id']
            request.data['user_id']
            request.data['to_user_id']
        except KeyError:
            res={"status":False,"message":"data missing event_id, user_id,to_user_id","data":{}}
            return Response(res,status=status.HTTP_200_OK)   
        event_id=request.data['event_id']
        user_id=request.data['user_id']
        to_user_id=request.data['to_user_id']
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        event=Event.objects.filter(id=event_id).first()
        if event is None:
            res={"status":False,"message":"Event not found","data":{}}
            return Response(res)
        serializer=EventSerializer(event)
        serializer_user=UserSerializer(user)
        date=serializer.data['event_start_date']
        if date:
            cDate=datetime.strptime(date,'%Y-%m-%d')
            date=cDate.strftime('%A, %B %d, %Y')
        else:
            date="today"    
        if serializer.data['name'] or date or serializer_user.data['first_name']  is None:
            desc="Someone shared event with you"
        else:
            desc="You have a shared event '"+serializer.data['name']+"' on "+date+" by @"+serializer_user.data['first_name']
        details={"has_button":False,"id":serializer.data['id']}    
        if to_user_id is not None:
            toUsersIds=to_user_id
            toUsers=toUsersIds
            for toUser in toUsers:            
                to_user=User.objects.filter(id=toUser).first()
                if to_user is None:
                    res={"status":False,"message":"To User not found","data":{}}
                    return Response(res)    
                Notification.objects.create(title="Event Shared With You!",description=desc,redirect_to="EVENT_PAGE",details=details,user_id=User.objects.get(id=toUser),created_by=user)
                sentToUserDevices=Device.objects.filter(user_id=toUser).all()
                if sentToUserDevices.count()>0:
                    device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                    for device in device_serializer.data:
                        if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                            fcm=Fcm()
                            fcm.send(device['fcm_token'],"Event Shared With You!",desc,{"redirect_to":"EVENT_PAGE"})              
            res={"status":True,"message":"Shared event successfully","data":{}}
            return Response(res)
        res={"status":False,"message":"to_user_id missing","data":{}}
        return Response(res,status=status.HTTP_200_OK)           


class VenueStatusAPIView(APIView):
    """Following are possible values for the status types
    \n"joined","liked","un_liked""
    """
    def get(self,request,venue_id,user_id,status):
        status_list = ["liked","un_liked","joined"]
        if status in status_list:
            venueStatus=VenueStatus.objects.filter(user_id=user_id,venue_id=venue_id).first()
            if venueStatus is not None:
                if status == "liked":
                    venueStatus.liked=True
                if status == "un_liked":
                    venueStatus.liked=False 
                if status == "joined":
                    venueStatus.joined=True   
                venueStatus.save();    
                res={"status":True,"message":"Venue status updated successfully","data":{}}
                return Response(res)
            else:
                if status == "liked":
                    VenueStatus.objects.create(user_id=User.objects.get(id=user_id),venue_id=Venue.objects.get(id=venue_id) ,liked=True)
                if status == "joined":
                    VenueStatus.objects.create(user_id=User.objects.get(id=user_id),venue_id=Venue.objects.get(id=venue_id) ,joined=True)
                if status == "un_liked":
                    VenueStatus.objects.create(user_id=User.objects.get(id=user_id),venue_id=Venue.objects.get(id=venue_id),liked=False)    
                res={"status":True,"message":"Venue status created successfully","data":{}}
                return Response(res)
        else:
            res={"status":False,"message":"Invalid status provided.","data":{'status_list':status_list}}
            return Response(res)
        
        
class EventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        eventStatusIds=EventStatus.objects.values_list('event_id',flat=True).filter(user_id=user_id).all()    
        events=Event.objects.filter((Q(user_id=user_id) | Q(pk__in=set(eventStatusIds))),archived=False).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            events_list=[]
            for event in serializer.data:
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
                eventStatusByUser=EventStatus.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                        eventTransactionByUser=EventTransaction.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                events_list.append(event)
            res={"status":True,"message":"events found","data":{"events":events_list}}
        else:
            res={"status":True,"message":"event not found","data":{"events":[]}}
        return Response(res)

class EventNearMeListAPIView(ListAPIView):
    def list(self, request,user_id,latitude,longitude, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        latitude = latitude
        longitude = longitude 
        query= "SELECT id,access_type,latitude, longitude, 3956 * 2 * ASIN(SQRT(POWER(SIN((%s - latitude) * 0.0174532925 / 2), 2) + COS(%s * 0.0174532925) * COS(latitude * 0.0174532925) * POWER(SIN((%s - longitude) * 0.0174532925 / 2), 2) )) as distance from events_event WHERE archived=0 and access_type='PUBLIC' and event_end_date>= date() group by id  having distance < 50  ORDER BY distance ASC " % ( latitude, latitude, longitude)
        events=Event.objects.raw(query)
        if len(events)> 0:
            serializer = EventSerializer(events, many=True)
            events_list=[]
            for event in serializer.data:
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
                eventStatusByUser=EventStatus.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                        eventTransactionByUser=EventTransaction.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                events_list.append(event)
            res={"status":True,"message":"events found","data":{"events":events_list}}
        else:
            res={"status":True,"message":"event not found","data":{"events":[]}}
        return Response(res)
class PastEventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        events=Event.objects.filter(user_id=user_id,event_end_date__lte=datetime.today(),archived=False).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            res={"status":True,"message":"events found","data":{"events":serializer.data}}
        else:
            res={"status":False,"message":"Not found","data":{}}
        return Response(res)
class UpcomingEventListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        events=Event.objects.filter(user_id=user_id,event_end_date__gte=datetime.today(),archived=False).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            res={"status":True,"message":"events found","data":{"events":serializer.data}}
        else:
            res={"status":False,"message":"Not found","data":{}}
        return Response(res)

class EventNotificaionStatusAPIView(ListAPIView):
    """
    Available statuses
    'accept/decline'
    """
    def list(self, request,user_id,notificaion_id,event_id,status, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        event=Event.objects.filter(pk=event_id).first()
        if event is None:
            res={"status":False,"message":"Event not found","data":{}}
            return Response(res)
        notification=Notification.objects.filter(id=notificaion_id).first()
        if notification is None:
            res={"status":False,"message":"Notification not found","data":{}}
            return Response(res)            
        eventStatus=EventStatus.objects.filter(user_id=user_id,event_id=event_id).first()
        if  status=='accept':
            if eventStatus is not None:
                eventStatus.joined=True
            else:
                EventStatus.objects.create(user_id=User.objects.get(id=user_id),event_id=Event.objects.get(id=event_id) ,joined=True)                 
            #
            details=notification.details
            if details:
                details=ast.literal_eval(details)
                details.update({"desc":"You have accepted event invite","action":"accepted"})
            notification.details=details
            notification.save()      
            res={"status":True,"message":"Event accepted successfully","data":{}}
        elif status=='decline':
            # 
            if eventStatus is not None:
                eventStatus.delete()
            details=notification.details
            if details:
                details=ast.literal_eval(details)
                details.update({"desc":"You have declined event invite","action":"declined"})
            notification.details=details
            notification.save()
            res={"status":True,"message":"Event declined successfully","data":{}}
        else:
            res={"status":False,"message":"provide valid status,'accept/decline'","data":{}}
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

class CreateVenueAPIView(CreateAPIView):
    """
    to create venue images pass
    venue_images[] along with other params
    """
    serializer_class=VenueSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Venue created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            if request.FILES.getlist('venue_images[]') is not None:
                venue_images=request.FILES.getlist('venue_images[]')
                for image in venue_images:
                    venueImage=VenueImage.objects.create(venue=Venue.objects.get(id=serializer.data['id']),image=image)
                    venueImage.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
# class VenueListAPIView(ListAPIView):
#     serializer_class=VenueSerializer
    
#     def get_queryset(self):
#         return Venue.objects.all()

class RequestVenueAPIView(CreateAPIView):
    """
    to create/request venue
    name,city
    """
    serializer_class=RequestVenueSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Venue requested successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)

class VenueListAPIView(ListAPIView):
    def list(self, request,user_id,latitude,longitude, *args, **kwargs):
        popular=False
        return venueCommon(self, request,user_id,popular,latitude,longitude, *args, **kwargs)    

class VenuePopularListAPIView(ListAPIView):
    def list(self, request,user_id,latitude,longitude, *args, **kwargs):
        popular=True
        return venueCommon(self, request,user_id,popular,latitude,longitude, *args, **kwargs)         
class VenueNearMeListAPIView(ListAPIView):
    def list(self, request,user_id,latitude,longitude, *args, **kwargs):
        popular=False
        return venueCommon(self, request,user_id,popular,latitude,longitude, *args, **kwargs)


def venueCommon(self, request,user_id,popular=None,latitude=None,longitude=None, *args, **kwargs):
    user=User.objects.filter(id=user_id).first()
    if user is None:
        res={"status":False,"message":"User not found","data":{}}
        return Response(res)
    venueCount=0
    if latitude is not None and longitude is not None:
        latitude = latitude
        longitude = longitude 
        query= "SELECT id,latitude, longitude, 3956 * 2 * ASIN(SQRT(POWER(SIN((%s - latitude) * 0.0174532925 / 2), 2) + COS(%s * 0.0174532925) * COS(latitude * 0.0174532925) * POWER(SIN((%s - longitude) * 0.0174532925 / 2), 2) )) as distance from events_venue where archived=0  group by id  having distance < 50  ORDER BY distance ASC " % ( latitude, latitude, longitude)
        venues=Venue.objects.raw(query)
        venueCount=len(venues)
    elif popular:
        venues=Venue.objects.filter(archived=False).all()
        venueCount=venues.count()
    else:    
        venues=Venue.objects.filter(archived=False).all()
        venueCount=venues.count()
    if venueCount > 0:
        serializer = VenueSerializer(venues, many=True)
        venue_list=[]
        if popular:
            venueDataList=sorted(serializer.data,key=lambda x:x['event_count'],reverse=True)
        else:
            venueDataList=serializer.data

        for venue in venueDataList:
            events=Event.objects.filter(venue=venue['id'],archived=False).all()
            liveEventCount=0
            if events.count() > 0:
                serializer = EventSerializer(events, many=True)
                events_list=[]
                for event in serializer.data:
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
                    status_list={'checked_in':False,'pinned':False,'liked':False,'paid':False,'guest_list':False,'invited':False}
                    eventStatusByUser=EventStatus.objects.filter(user_id=user_id,event_id=event['id']).first()    
                    if eventStatusByUser is not None:
                        if eventStatusByUser.checked_in:
                            status_list['checked_in']=True
                        if eventStatusByUser.pinned:
                            status_list['pinned']=True
                        if eventStatusByUser.liked:
                            status_list['liked']=True    
                        if eventStatusByUser.paid:
                            status_list['paid']=True
                        # transaction
                        eventTransactionByUser=EventTransaction.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                            liveEventCount+=1
                    event['is_live']=isLive
                    events_list.append(event)
                venue['events']=events_list
                venueStatus={'liked':False,'joined':False}
                venueStatusByUser=VenueStatus.objects.filter(user_id=user_id,venue_id=venue['id']).first() 
                if venueStatusByUser is not None:
                     if venueStatusByUser.liked:
                        venueStatus['liked']=True
                     if venueStatusByUser.joined:
                            venueStatus['joined']=True 
                venue['venue_status']=venueStatus              
                venue['has_live_event']=True if liveEventCount > 0 else False              
                venue_list.append(venue)
                res={"status":True,"message":"venue found","data":{"venues":venue_list}}
            else:
                venue['events']=[]
                venueStatus={'liked':False,'joined':False}
                venueStatusByUser=VenueStatus.objects.filter(user_id=user_id,venue_id=venue['id']).first() 
                if venueStatusByUser is not None:
                     if venueStatusByUser.liked:
                        venueStatus['liked']=True
                     if venueStatusByUser.joined:
                            venueStatus['joined']=True 
                venue['venue_status']=venueStatus 
                venue['has_live_event']=True if liveEventCount > 0 else False               
                venue_list.append(venue)
                res={"status":True,"message":"event not found","data":{"venues":venue_list}}
    else:
        res={"status":True,"message":"venue not found","data":{"venues":[]}}
    return Response(res)

class VenueDetailAPIView(APIView):
    def get(self,request,venue_id,user_id):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)

        venue=Venue.objects.filter(id=venue_id).first()    
        if venue is None:
            res={"status":False,"message":"Venue not found","data":{}}
            return Response(res)
        venueData=VenueSerializer(venue)
        venue=venueData.data
        events=Event.objects.filter(venue=venue['id'],archived=False).all()
        liveEventCount=0
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            events_list=[]
            for event in serializer.data:
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
                status_list={'checked_in':False,'pinned':False,'liked':False,'paid':False,'guest_list':False,'invited':False}
                eventStatusByUser=EventStatus.objects.filter(user_id=user_id,event_id=event['id']).first()    
                if eventStatusByUser is not None:
                    if eventStatusByUser.checked_in:
                        status_list['checked_in']=True
                    if eventStatusByUser.pinned:
                        status_list['pinned']=True
                    if eventStatusByUser.liked:
                        status_list['liked']=True    
                    if eventStatusByUser.paid:
                        status_list['paid']=True
                        # transaction
                        eventTransactionByUser=EventTransaction.objects.filter(user_id=user_id,event_id=event['id']).first()    
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
                        liveEventCount+=1
                event['is_live']=isLive
                events_list.append(event)
            venue['events']=events_list
            venueStatus={'liked':False,'joined':False}
            venueStatusByUser=VenueStatus.objects.filter(user_id=user_id,venue_id=venue['id']).first() 
            if venueStatusByUser is not None:
                if venueStatusByUser.liked:
                    venueStatus['liked']=True
                    if venueStatusByUser.joined:
                        venueStatus['joined']=True 
            venue['venue_status']=venueStatus              
            venue['has_live_event']=True if liveEventCount > 0 else False              
            res={"status":True,"message":"venue found","data":{"venue":venue}}
        else:
            venue['events']=[]
            venueStatus={'liked':False,'joined':False}
            venueStatusByUser=VenueStatus.objects.filter(user_id=user_id,venue_id=venue['id']).first() 
            if venueStatusByUser is not None:
                if venueStatusByUser.liked:
                    venueStatus['liked']=True
                    if venueStatusByUser.joined:
                        venueStatus['joined']=True 
            venue['venue_status']=venueStatus 
            venue['has_live_event']=True if liveEventCount > 0 else False 
            res={"status":True,"message":"venue found with no events","data":{"venue":venue}}

        return Response(res)                 
                
class VenueAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=VenueSerializer
    lookup_field="id"     
    queryset = Venue.objects.all()

# class CreateVenueAPIView(CreateAPIView):
#     serializer_class=VenueSerializer

#     def perform_create(self, serializer):
#         return super().perform_create(serializer)    


def is_between(time, time_range):
    if time_range[1] < time_range[0]:
       return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]        