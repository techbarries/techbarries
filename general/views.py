import ast
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView,ListAPIView
from authentication.models import Device, User
from authentication.serializers import DeviceSerializer, UserSerializer
from events.models import Event, EventStatus
from fcm import Fcm
from general.models import Faq, Friends, InviteFriends, Notification
from general.serializers import FaqSerializer, FriendsSerializer, InviteFriendsSerializer, NotificationSerializer, ReportSerializer
from django.db.models import Q
from authentication.twilio import Twilio
from rest_framework.views import APIView



# Create your views here.
class CreateNotificationAPIView(CreateAPIView):
    """Possible values for redirect_to
    \n
    'EVENT_PAGE',
    'EVENT_GUEST_LIST_PAGE',
    'CHAT_PAGE',
    'FRIEND_PROFILE_PAGE',
    'MY_WALLET_PAGE',
    'MY_WALLET_TICKET_PAGE',
    'REPORT_PAGE'
    
    """
    serializer_class=NotificationSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Notification created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
class DeleteNotificationAPIView(APIView):
    def delete(self,request,id, *args, **kwargs):
         notification=Notification.objects.filter(id=id).first()
         if notification is not None:
            notification.delete()
            res={"status":True,"message":"Notification deleted successfully","data":{}}
         else:
            res={"status":False,"message":"Notification not found","data":{}}
         return Response(res,status=status.HTTP_200_OK)     
class NotificationListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        notifications=Notification.objects.filter(user_id=user_id).all()
        if notifications.count() > 0:
            serializer = NotificationSerializer(notifications, many=True)
            notification_list=[]
            for device in serializer.data:
                if device['details'] is not None:
                    try:
                        json_data = ast.literal_eval(device['details'])
                        json_data['button_clicked']=""
                        device['details']= json_data
                    except:
                        device['details']= device['details']
                notification_list.append(device)
            res={"status":True,"message":"notifications found","data":{"notifications":notification_list}}

        else:
            res={"status":True,"message":"notifications not found","data":{"notifications":[]}}
        return Response(res) 

class FaqListApiView(ListAPIView):
    def list(self, request, *args, **kwargs):
        faq=Faq.objects.all()
        if faq is None or faq.count() < 1:
            res={"status":False,"message":"Faq not found","data":{}}
            return Response(res)
        seriliazer=FaqSerializer(faq,many=True)
        res={"status":True,"message":"faqs found","data":{"faqs":seriliazer.data}}
        return Response(res) 
class NotificationMarkReadAPIView(ListAPIView):
    def list(self, request,user_id,id=None, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        if id is not None:
            notification=Notification.objects.filter(pk=id,user_id=user_id).first()
            if notification is not None:
                notification.status=True
                notification.save()
                res={"status":True,"message":"notification mark as read successfully","data":{}}
            else:   
                res={"status":True,"message":"notification not found","data":{}}
        else:
            notifications=Notification.objects.filter(user_id=user_id).all()
            if notifications.count() > 0:
                notifications=Notification.objects.filter(user_id=user_id).update(status=True)
                res={"status":True,"message":"notifications mark as read successfully","data":{}}
            else:
                res={"status":True,"message":"notifications not found","data":{}}
        return Response(res)

class NotificationAPIView(ListAPIView):
    def list(self, request,*args, **kwargs):
        notifications=Notification.objects.all()
        if notifications.count() > 0:
            serializer = NotificationSerializer(notifications, many=True)
            notification_list=[]
            for device in serializer.data:
                if device['details'] is not None:
                    try:
                        json_data = ast.literal_eval(device['details'])
                        json_data['button_clicked']=""
                        device['details']= json_data
                    except:
                        device['details']= device['details']
                notification_list.append(device)
            res={"status":True,"message":"notifications found","data":{"notifications":notification_list}}
        else:
            res={"status":True,"message":"notifications not found","data":{"notifications":[]}}
        return Response(res)

class CreateFriendRequestAPIView(CreateAPIView):
    serializer_class=FriendsSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Friend Request created successfully","data":{}}
        if serializer.is_valid():
            alreadyExists=Friends.objects.filter(Q(sent_by_user_id=request.data['sent_by_user_id'],sent_to_user_id=request.data['sent_to_user_id']) | Q(sent_by_user_id=request.data['sent_to_user_id'],sent_to_user_id=request.data['sent_by_user_id']) ).all()
            if alreadyExists.count()>0:
                res={"status":False,"message":"Already friend request exists.","data":{}}
                return Response(res)
            serializer.save()
            res.update(data=serializer.data)
            # 
            user=User.objects.filter(pk=request.data['sent_by_user_id']).first()
            if user is not None:
                serializer_user=UserSerializer(user)
                desc="@"+serializer_user.data['first_name']+" has added you as a friend. Click to confirm"
                details={"has_button":True,"button_count":2,"positive_button":"Accept","negative_button":"Decline","type":"FRIEND_REQUEST","id":serializer.data['id'],"desc":"","action":None}
                notification=Notification.objects.create(title="New friend request!",description=desc,redirect_to="FRIEND_PROFILE_PAGE",details=details,user_id=User.objects.get(id=request.data['sent_to_user_id']),created_by=user)
                friendRequest=Friends.objects.filter(pk=serializer.data['id']).first()
                friendRequest.notification=notification
                friendRequest.save()
                sentToUserDevices=Device.objects.filter(user_id=request.data['sent_to_user_id']).all()
                if sentToUserDevices.count()>0:
                    device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                    for device in device_serializer.data:
                        if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                            fcm=Fcm()
                            fcm.send(device['fcm_token'],"New friend request!",desc,{"redirect_to":"FRIEND_PROFILE_PAGE"})
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)

class InviteByPhoneAPIView(CreateAPIView):
    serializer_class=InviteFriendsSerializer
    def post(self,request):
        msg=""
        try:
            user_id=request.data['sent_by_user_id']
            user=User.objects.filter(id=user_id).first()
            if user is None:
                res={"status":False,"message":"User not found","data":{}}
                return Response(res)
            if user.first_name is not None and  len(user.first_name)>0:
                msg="You are invited to download Pulse APP by "+user.first_name+". Clicking the link: https://google.com"
            else:
                msg="You are invited to download Pulse APP by clicking the link: https://google.com"
        except KeyError:
            msg="You are invited to download Pulse APP by clicking the link: https://google.com"
        if request.data['phone_number'] is not None:
            phoneNumbers=request.data['phone_number']
            phoneNumbers=phoneNumbers.split(",")
            for phone in phoneNumbers:
                userExists=User.objects.filter(phone_number=phone).first()
                if userExists is None:
                    InviteFriends.objects.create(phone_number=phone,sent_by_user_id=User.objects.get(id=request.data['sent_by_user_id']))
                    twilio=Twilio(msg,phone)
                    smsResponse=twilio.send()
        res={"status":False,"message":"Sms sent to phone numbers.","data":{}}
        return Response(res,status=status.HTTP_200_OK)        
        

class FriendRequestsListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        friendRequests=Friends.objects.filter(sent_to_user_id=user_id,status=False).all()
        if friendRequests.count() > 0:
            serializer =  FriendsSerializer(friendRequests, many=True)
            friendRequestsList=[]
            for friendrequest in serializer.data:
                user=User.objects.filter(id=friendrequest['sent_by_user_id']).first()
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
                    friendrequest['sent_by_user']=userItem
                friendRequestsList.append(friendrequest)
            res={"status":True,"message":"friendRequests found","data":{"friend_requests":friendRequestsList}}

        else:
            res={"status":True,"message":"friendRequests not found","data":{"friend_requests":[]}}
        return Response(res)     

class FriendsListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        friends=Friends.objects.filter(Q(sent_to_user_id=user_id )|Q(sent_by_user_id=user_id ),status=True).all()
        if friends.count() > 0:
            serializer =  FriendsSerializer(friends, many=True)
            friendsList=[]
            for friend in serializer.data:
                if friend['sent_by_user_id']==user_id:
                    user=User.objects.filter(id=friend['sent_to_user_id']).first()
                else:   
                    user=User.objects.filter(id=friend['sent_by_user_id']).first()
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
                    friend['friend_user']=userItem
                    
                friendsList.append(friend)
            res={"status":True,"message":"friends found","data":{"friends":friendsList}}

        else:
            res={"status":True,"message":"friends not found","data":{"friends":[]}}
        return Response(res)

class FriendRequestStatusAPIView(ListAPIView):
    """
    Available statuses
    'accept/decline/un_friend'
    """
    def list(self, request,id,status, *args, **kwargs):
        friendRequest=Friends.objects.filter(pk=id).first()
        if friendRequest is None:
            res={"status":False,"message":"friendRequest not found","data":{}}
            return Response(res)
        if  status=='accept':
            if friendRequest.status:
                res={"status":False,"message":"friendRequest already accepted","data":{}}
                return Response(res)
            friendRequest.status=True
            # 
            if friendRequest.notification is not None:
                notification=Notification.objects.filter(pk=friendRequest.notification.id).first()
                if notification is not None:
                    details=notification.details
                    if details:
                        details=ast.literal_eval(details)
                        details.update({"desc":"You have accepted friend request","action":"accepted"})
                    notification.details=details
                    notification.save()
            friendRequest.save()
            sentToUserDevices=Device.objects.filter(user_id=friendRequest.sent_by_user_id.id).all()
            if sentToUserDevices.count()>0:
                user=User.objects.filter(id=friendRequest.sent_to_user_id.id).first()
                desc="Friend request successfully accepted you sent."
                if user.first_name is not None and  len(user.first_name)>0:
                    desc="Friend request sent to @"+user.first_name+" is accepted."
                device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                for device in device_serializer.data:
                    if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                        fcm=Fcm()
                        fcm.send(device['fcm_token'],"Friend request accepted",desc,{"redirect_to":"FRIEND_PROFILE_PAGE"})
        
            res={"status":True,"message":"friendRequest accepted successfully","data":{}}
        elif status=='decline':
            # 
            if friendRequest.notification is not None:
                notification=Notification.objects.filter(pk=friendRequest.notification.id).first()
                if notification is not None:
                    details=notification.details
                    if details:
                        details=ast.literal_eval(details)
                        details.update({"desc":"You have declined friend request","action":"declined"})
                    notification.details=details
                    notification.save()
            sentToUserDevices=Device.objects.filter(user_id=friendRequest.sent_by_user_id.id).all()
            if sentToUserDevices.count()>0:
                user=User.objects.filter(id=friendRequest.sent_to_user_id.id).first()
                desc="Friend request declined you sent."
                if user.first_name is not None and  len(user.first_name)>0:
                    desc="Friend request sent to @"+user.first_name+" is declined."
                device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                for device in device_serializer.data:
                    if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                        fcm=Fcm()
                        fcm.send(device['fcm_token'],"Friend request declined",desc,{"redirect_to":"FRIEND_PROFILE_PAGE"})        
            friendRequest.delete()
            res={"status":True,"message":"friendRequest declined successfully","data":{}}
        elif status=='un_friend':
            # friendRequest.delete()
            if not friendRequest.status:
                res={"status":False,"message":"already unfriend","data":{}}
                return Response(res)
            friendRequest.status=False
            # 
            if friendRequest.notification is not None:
                notification=Notification.objects.filter(pk=friendRequest.notification.id).first()
                if notification is not None:
                    details=notification.details
                    if details:
                        details=ast.literal_eval(details)
                        details.update({"desc":"","action":None})
                    notification.details=details
                    notification.save()
            friendRequest.save()
            sentToUserDevices=Device.objects.filter(user_id=friendRequest.sent_by_user_id.id).all()
            if sentToUserDevices.count()>0:
                user=User.objects.filter(id=friendRequest.sent_to_user_id.id).first()
                desc="One of your friend has un-friend you."
                if user.first_name is not None and  len(user.first_name)>0:
                    desc="One of your friend  @"+user.first_name+" has un-friend you."
                device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                for device in device_serializer.data:
                    if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                        fcm=Fcm()
                        fcm.send(device['fcm_token'],"Friend un-friend",desc,{"redirect_to":"FRIEND_PROFILE_PAGE"})             
            res={"status":True,"message":"friendRequest un_friend successfully","data":{}}    
        else:
            res={"status":False,"message":"provide valid status,'accept/decline/un_friend'","data":{}}
        return Response(res)


# Create your views here.
class CreateReportAPIView(CreateAPIView):
    """
    Possible values for report_type
    'Users','Events','Venues','Ticket',

    report_type_id is the selected instance id i.e User=>user_id
    
    Possible values for report_reason
    'Unprofessional','Fake','Scam','Spam','False_Information','Nudity','Underage_Drinking','Violence','Hate','Dangerous_Organization','Bullying','Illegal','Suicide'
    """
    serializer_class=ReportSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Reported successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            #notificaion
            data=serializer.data 
            if data["report_type"]=="Users":
                if data["report_type_id"] is not None:
                    user=User.objects.filter(id=data["report_type_id"]).first()
                    if user is not None:
                        details={"has_button":False,"id":user.id}
                        desc="Your account has been reported for "+data["report_reason"]+" reason"
                        Notification.objects.create(title="Account Reported",description=desc,redirect_to="Report_PAGE",details=details,user_id=User.objects.get(id=user.id))
                        sentToUserDevices=Device.objects.filter(user_id=user.id).all()
                        if sentToUserDevices.count()>0:
                            device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                            for device in device_serializer.data:
                                if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                                    fcm=Fcm()
                                    fcm.send(device['fcm_token'],"Account Reported",desc,{"redirect_to":"Report_PAGE"})
            if data["report_type"]=="Events":
                if data["report_type_id"] is not None:
                    event=Event.objects.filter(id=data["report_type_id"]).first()
                    details={"has_button":False,"id":event.user_id.id}
                    desc="Your Event '"+event.name+"' was reported for "+data["report_reason"]+" reason. Please make changes immediately."
                    Notification.objects.create(title= event.name+" - Event Reported",description=desc,redirect_to="Report_PAGE",details=details,user_id=User.objects.get(id=event.user_id.id))
                    sentToUserDevices=Device.objects.filter(user_id=event.user_id.id).all()
                    if sentToUserDevices.count()>0:
                        device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                        for device in device_serializer.data:
                            if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                                fcm=Fcm()
                                fcm.send(device['fcm_token'],event.name+" - Event Reported",desc,{"redirect_to":"Report_PAGE"})

            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)