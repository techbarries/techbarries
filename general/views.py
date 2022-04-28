from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView,ListAPIView
from authentication.models import User
from general.models import Notification
from general.serializers import NotificationSerializer

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
                notification_list.append(device)
            res={"status":True,"message":"notifications found","data":{"notifications":notification_list}}

        else:
            res={"status":True,"message":"notifications not found","data":{"notifications":[]}}
        return Response(res) 

class NotificationAPIView(ListAPIView):
    def list(self, request,*args, **kwargs):
        notifications=Notification.objects.all()
        if notifications.count() > 0:
            serializer = NotificationSerializer(notifications, many=True)
            notification_list=[]
            for device in serializer.data:
                notification_list.append(device)
            res={"status":True,"message":"notifications found","data":{"notifications":notification_list}}
        else:
            res={"status":True,"message":"notifications not found","data":{"notifications":[]}}
        return Response(res) 