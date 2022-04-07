from ast import Not
from datetime import datetime,timezone
from email import message
import imp
from telnetlib import STATUS
from urllib import response
from rest_framework.generics import GenericAPIView,CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from authentication.models import Device, SmsOTP, User
from authentication.serializers import DeviceSerializer, PulseUserSerializer, UserSerializer
from rest_framework import response,status
from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
import random

from authentication.twilio import Twilio
# Create your views here.

class PulseUserAPIView(GenericAPIView):
    serializer_class=PulseUserSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"User created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
        # return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(ListAPIView):
    serializer_class=UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(is_active=1)

class CreateDeviceAPIView(CreateAPIView):
    serializer_class=DeviceSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class DeviceListAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=DeviceSerializer
    lookup_field="id"
    queryset = Device.objects.all()

class DeviceAPIView(ListAPIView):
    serializer_class=DeviceSerializer
    def get_queryset(self):
            return Device.objects.all()
            
class DeviceByUserView(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    lookup_field = 'user_id'
    def get_queryset(self):
        user_id = self.request.parser_context['kwargs'].get('user_id')
        return Device.objects.all().filter(user_id=user_id)
    # filter_backends = (DjangoFilterBackend,)
    # search_fields = ['user_id']

# class UserByTokenView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     lookup_field = 'user_token'
#     def get_queryset(self):
#         user_token = self.request.parser_context['kwargs'].get('user_token')
#         return User.objects.all().filter(user_token=user_token)

class UserByTokenView(APIView):
    serializer_class=PulseUserSerializer
    def get(self,request,uid,format=None):
        uid=uid
        res={"status":True,"message":"User found","data":{}}
        if uid is not None:
            user=User.objects.filter(uid=uid).first()
            if user is not None:
                serializer=UserSerializer(user)
                res.update(data=serializer.data)
                return Response(res)
        res.update(status=False,message="Not found")
        return Response(res)

class GenerateSmsOTP(APIView):
    def get(self,request,phone):
        phoneNumber=SmsOTP.objects.filter(phone=phone).first()
        otp = random.randint(1000, 9999)
        if phoneNumber is not None:
            delta=datetime.now(timezone.utc)-phoneNumber.updated_at
            delta=delta.total_seconds()/ (60 * 60)
            delta=round(delta,1)
            if phoneNumber.counter > 5 and delta < 1:
                res={"status":False,"message":"Too many tries.Can try after 1 hour.","data":{"counter":phoneNumber.counter}}
                return Response(res)
            elif phoneNumber.counter > 5 and delta > 0:
                phoneNumber.counter=0
            else:
                phoneNumber.counter+=1
            phoneNumber.otp=otp
            phoneNumber.is_verified=0
            phoneNumber.save()
            twilio=Twilio("Your Otp Code is:"+str(otp),phone)
            smsResponse=twilio.send()
            if smsResponse==1:
                res={"status":True,"message":"Otp sent successfully","data":{"otp":otp,"counter":phoneNumber.counter,"delta": delta}}
                return Response(res)
            elif smsResponse==2:   
                res={"status":False,"message":"Twilio Unable to send otp.","data":{}}
                return Response(res)
            else:
                res={"status":False,"message":"Invalid phone number.","data":{}}
                return Response(res)        
        else:  
            SmsOTP.objects.create(phone=phone,otp=otp,is_verified=0)
            twilio=Twilio("Your Otp Code is:"+str(otp),phone)
            smsResponse=twilio.send()
            if smsResponse==1:
                res={"status":True,"message":"Otp sent successfully","data":{"otp":otp}}
                return Response(res)
            elif smsResponse==2:   
                res={"status":False,"message":"Twilio Unable to send otp.","data":{}}
                return Response(res)
            else:
                res={"status":False,"message":"Invalid phone number.","data":{}}
                return Response(res)
                
class VerifySmsOTP(APIView):        
    @staticmethod
    def post(request,phone,otp):
        if otp is None:
            res={"status":False,"message":"Otp is required","data":{}}
            return Response(res)
        phoneNumber=SmsOTP.objects.filter(phone=phone,otp=otp,is_verified=0).first()
        if phoneNumber is not None:
            phoneNumber.is_verified=1
            phoneNumber.save()
            res={"status":True,"message":"Otp verified successfully","data":{}}
            return Response(res)
        res={"status":False,"message":"Invalid otp.","data":{}}
        return Response(res)
 


            

            

        
