from datetime import datetime,timezone
from rest_framework.generics import GenericAPIView,CreateAPIView,ListAPIView
from authentication.models import Device, SmsOTP, User, UserCardBilling
from authentication.serializers import DeviceSerializer, PulseUserSerializer, UserCardBillingSerializer, UserDetailSerializer, UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import random,GlobalConstant

from authentication.twilio import Twilio
from events.models import EventStatus, University
from events.serializers import UniversitySerializer
# Create your views here.

class PulseUserAPIView(GenericAPIView):
    serializer_class=PulseUserSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":GlobalConstant.Data["user_created"],"data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message=GlobalConstant.Data["validation_error"].replace("#type#","User"),data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
        # return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        try:
            request.data['id']
        except KeyError:
            res={"status":False,"message":GlobalConstant.Data["update_data_id_required"],"data":{}}
            return Response(res,status=status.HTTP_200_OK) 
        user=User.objects.filter(pk=request.data['id']).first()
        if user is None:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
            return Response(res)
        serializer=PulseUserSerializer(user,data=request.data)  
        res={"status":True,"message":GlobalConstant.Data["user_updated"],"data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message=GlobalConstant.Data["validation_update_error"].replace("#type#","User"),data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)           

class DeleteUserAPIView(APIView):
    def delete(self,request,id, *args, **kwargs):
        user=User.objects.filter(id=id).first()
        if user is not None and user.is_active:
            user.delete()
            res={"status":True,"message":GlobalConstant.Data["user_deleted"],"data":{}}
        else:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
        return Response(res,status=status.HTTP_200_OK)
class UserListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        users=User.objects.filter(is_active=1,is_superuser=False).all()
        if users.count() > 0:
            serializer = UserSerializer(users, many=True)
            userList=[]
            for user in serializer.data:
                # if user['university'] is not None:
                #     university=University.objects.filter(pk=user['university']).first()
                #     if university is not None:
                #         serializer=UniversitySerializer(university)
                #         user['university']=serializer.data
                userList.append(user)
            res={"status":True,"message":GlobalConstant.Data["user_exists"],"data":{"users":userList}}
        else:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
        return Response(res)
    # def get_queryset(self):
    #     return User.objects.filter(is_active=1)

class CreateDeviceAPIView(CreateAPIView):
    serializer_class=DeviceSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":GlobalConstant.Data["device_created"],"data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message=GlobalConstant.Data["validation_error"].replace("#type#","Device"),data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
    # def perform_create(self, serializer):
    #     return super().perform_create(serializer)

class DeviceListAPIView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
            return Response(res)
        devices=Device.objects.filter(user_id=user_id).all()
        if devices.count() > 0:
            serializer = DeviceSerializer(devices, many=True)
            device_list=[]
            for device in serializer.data:
                device_list.append(device)
            res={"status":True,"message":GlobalConstant.Data["device_exists"],"data":{"devices":device_list}}

        else:
            res={"status":True,"message":GlobalConstant.Data["device_not_exists"],"data":{"devices":[]}}
        return Response(res) 

class DeviceAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        devices=Device.objects.all()
        if devices.count() > 0:
            serializer = DeviceSerializer(devices, many=True)
            device_list=[]
            for device in serializer.data:
                device_list.append(device)
            res={"status":True,"message":GlobalConstant.Data["device_exists"],"data":{"devices":device_list}}
        else:
            res={"status":True,"message":GlobalConstant.Data["device_not_exists"],"data":{"devices":[]}}
        return Response(res) 
            
class DeviceByUserView(ListAPIView):
    def list(self, request,user_id, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
            return Response(res)
        devices=Device.objects.filter(user_id=user_id).all()
        if devices.count() > 0:
            serializer = DeviceSerializer(devices, many=True)
            device_list=[]
            for device in serializer.data:
                device_list.append(device)
            res={"status":True,"message":GlobalConstant.Data["device_exists"],"data":{"devices":device_list}}

        else:
            res={"status":True,"message":GlobalConstant.Data["device_not_exists"],"data":{"devices":[]}}
        return Response(res) 

    # serializer_class = DeviceSerializer
    # lookup_field = 'user_id'
    # def get_queryset(self):
    #     user_id = self.request.parser_context['kwargs'].get('user_id')
    #     return Device.objects.all().filter(user_id=user_id)
    # filter_backends = (DjangoFilterBackend,)
    # search_fields = ['user_id']

# class UserByTokenView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     lookup_field = 'user_token'
#     def get_queryset(self):
#         user_token = self.request.parser_context['kwargs'].get('user_token')
#         return User.objects.all().filter(user_token=user_token)
class DetailUserAPIView(APIView):
    serializer_class=UserDetailSerializer()
    def get(self,request,user_id,format=None):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
            return Response(res)
        serializer=UserDetailSerializer(user)
        res={"status":True,"message":GlobalConstant.Data["user_exists"],"data":{"data":serializer.data}}
        return Response(res)

class UserByTokenView(APIView):
    serializer_class=PulseUserSerializer
    def get(self,request,uid,format=None):
        uid=uid
        res={"status":True,"message":GlobalConstant.Data["user_exists"],"data":{}}
        if uid is not None:
            user=User.objects.filter(uid=uid).first()
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
                # if user.university is not None:
                #     serializer=UniversitySerializer(user.university)
                #     userItem.update({"university":serializer.data})
                res.update(data=userItem)
                return Response(res)
        res.update(status=False,message=GlobalConstant.Data["user_not_exists"])
        return Response(res)

class GenerateSmsOTP(APIView):
    def get(self,request,phone):
        phoneNumber=SmsOTP.objects.filter(phone=phone).first()
        otp = random.randint(1000, 9999)
        if phoneNumber is not None:
            phoneNumber.otp=otp
            phoneNumber.is_verified=0
            phoneNumber.save()
            twilio=Twilio("Your Otp Code is:"+str(otp),phone)
            smsResponse=twilio.send()
            if smsResponse==1:
                res={"status":True,"message":GlobalConstant.Data["otp_sent"],"data":{"otp":otp,"counter":phoneNumber.counter}}
                return Response(res)
            elif smsResponse==2:   
                res={"status":False,"message":GlobalConstant.Data["twilio_unable_to_send"],"data":{}}
                return Response(res)
            else:
                res={"status":False,"message":GlobalConstant.Data["invalid_phone_number"],"data":{}}
                return Response(res)        
        else:  
            SmsOTP.objects.create(phone=phone,otp=otp,is_verified=0)
            twilio=Twilio("Your Otp Code is:"+str(otp),phone)
            smsResponse=twilio.send()
            if smsResponse==1:
                res={"status":True,"message":GlobalConstant.Data["otp_sent"],"data":{"otp":otp}}
                return Response(res)
            elif smsResponse==2:   
                res={"status":False,"message":GlobalConstant.Data["twilio_unable_to_send"],"data":{}}
                return Response(res)
            else:
                res={"status":False,"message":GlobalConstant.Data["invalid_phone_number"],"data":{}}
                return Response(res)
                
class VerifySmsOTP(APIView):        
    @staticmethod
    def post(request,phone,otp):
        if otp is None:
            res={"status":False,"message":GlobalConstant.Data["otp_required"],"data":{}}
            return Response(res)
        phoneNumber=SmsOTP.objects.filter(phone=phone,is_verified=0).first()
        if phoneNumber is not None:
            if phoneNumber.otp !=otp:
                delta=datetime.now(timezone.utc)-phoneNumber.updated_at
                delta=delta.total_seconds()/ (60 * 60)
                delta=round(delta,1)
                if phoneNumber.counter > 5 and delta < 1:
                    res={"status":False,"message":GlobalConstant.Data["too_many_tries"],"data":{"counter":phoneNumber.counter}}
                    return Response(res)
                elif phoneNumber.counter > 5 and delta > 0:
                    phoneNumber.counter=0
                else:
                    phoneNumber.counter+=1
                phoneNumber.save()
                res={"status":False,"message":GlobalConstant.Data["invalid_otp"],"data":{}}
                return Response(res)    
            phoneNumber.is_verified=1
            phoneNumber.save()
            res={"status":True,"message":GlobalConstant.Data["otp_verified"],"data":{}}
            return Response(res)
        res={"status":False,"message":GlobalConstant.Data["invalid_otp"],"data":{}}
        return Response(res)
 

class CreateCardBillingAPIView(CreateAPIView):
    serializer_class=UserCardBillingSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":GlobalConstant.Data["card_billing_created"],"data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message=GlobalConstant.Data["validation_error"].replace("#type#","Card"),data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)
            

class CardBillingListAPIView(ListAPIView):
    def list(self, request,user_id,otp, *args, **kwargs):
        user=User.objects.filter(id=user_id).first()
        if user is None:
            res={"status":False,"message":GlobalConstant.Data["user_not_exists"],"data":{}}
            return Response(res)
        phone=user.phone_number
        if phone is None or len(phone)==0:
            res={"status":False,"message":GlobalConstant.Data["user_phone_not_found"],"data":{}}
            return Response(res)
        smsOtp=SmsOTP.objects.filter(phone=user.phone_number,otp=otp,is_verified=0).first()    
        if smsOtp is None:
            res={"status":False,"message":GlobalConstant.Data["invalid_otp"],"data":{}}
            return Response(res)
        smsOtp.is_verified=1
        smsOtp.save()
        cardBillings=UserCardBilling.objects.filter(user_id=user_id).all()
        if cardBillings.count() > 0:
            serializer = UserCardBillingSerializer(cardBillings, many=True)
            card_billing_list=[]
            for card in serializer.data:
                card_billing_list.append(card)
            res={"status":True,"message":GlobalConstant.Data["card_exists"],"data":{"cards":card_billing_list}}

        else:
            res={"status":True,"message":GlobalConstant.Data["card_not_exists"],"data":{"cards":[]}}
        return Response(res)             

        
