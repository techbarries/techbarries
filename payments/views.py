from decouple import config
from django.shortcuts import render
import stripe
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import Device, User
from authentication.serializers import DeviceSerializer
from events.models import Event
from fcm import Fcm
from general.models import Notification

from payments.serializers import EventTransactionSerializer

# Create your views here.
class CreatePaymentIntentAPIView(APIView):
    """ 'amount':360 """
    def post(self,request):
        try:
            request.data['amount']
        except KeyError:
            res={"status":False,"message":"amount param is missing","data":{}}
            return Response(res,status=status.HTTP_200_OK)      

        try:
            # Create a PaymentIntent with the order amount and currency
            stripe.api_key=config('stripe_api_key')
            intent = stripe.PaymentIntent.create(
                amount=request.data['amount'],
                currency='cad',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
        except Exception as e:
            res={"status":False,"message":str(e),"data":{}}
            return Response(res,status=status.HTTP_200_OK)      
                
        res={"status":True,"message":"Payment intent created successfully","data":{"client_secret":intent['client_secret']}}
        return Response(res,status=status.HTTP_200_OK)


class CreateEventTransactionAPIView(CreateAPIView):
    """event_id, user_id, transaction_id, payment_status,payment_method,currency, bottle_fee, cover_fee, no_of_tickets, processing_fee, pulse_service_charges
    {
    "transaction_id": "pi_3LJLskFHPjA97y331KajVLja",
    "event_id":1,
    "user_id":2,
    "payment_status":true,
    "payment_method":"Stripe",
    "currency":"CAD",
    "bottle_fee":20,
    "cover_fee":12,
    "no_of_tickets":1,
    "processing_fee":10,
    "pulse_service_charges":20
    
}"""
    serializer_class=EventTransactionSerializer
    def post(self,request):
        try:
            request.data['user_id']
            request.data['event_id']
        except KeyError:
            res={"status":False,"message":"user_id,event_id required","data":{}}
            return Response(res,status=status.HTTP_200_OK)
        user=User.objects.filter(id=request.data["user_id"]).first()
        if user is None:
            res={"status":False,"message":"User not found","data":{}}
            return Response(res)
        event=Event.objects.filter(id=request.data["event_id"]).first()
        if event is None:
            res={"status":False,"message":"Event not found","data":{}}
            return Response(res)
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Event transaction created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            # notificaion to users
            desc="Your payment for the event '"+event.name+"' was successful."
            details={"has_button":False,"id":event.id}
            Notification.objects.create(title=event.name+" Event Payment Confirmation",description=desc,redirect_to="TICKET_WALLET_PAGE",details=details,user_id=User.objects.get(id=user.id))
            sentToUserDevices=Device.objects.filter(user_id=user.id).all()
            if sentToUserDevices.count()>0:
                device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                for device in device_serializer.data:
                    if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                        fcm=Fcm()
                        fcm.send(device['fcm_token'],event.name+" Event Payment Confirmation",desc,{"redirect_to":"TICKET_WALLET_PAGE"})                

            if serializer.data["bottle_fee"]>0:
                desc="Your purchase for event '"+event.name+"' was successful."
                details={"has_button":False,"id":event.id}
                Notification.objects.create(title=event.name+" Event purchase Confirmation",description=desc,redirect_to="TICKET_WALLET_PAGE",details=details,user_id=User.objects.get(id=user.id))
                sentToUserDevices=Device.objects.filter(user_id=user.id).all()
                if sentToUserDevices.count()>0:
                    device_serializer=DeviceSerializer(sentToUserDevices,many=True)
                    for device in device_serializer.data:
                        if device['fcm_token'] is not None and len(device['fcm_token'])>0:
                            fcm=Fcm()
                            fcm.send(device['fcm_token'],event.name+" Event purchase Confirmation",desc,{"redirect_to":"TICKET_WALLET_PAGE"})                 



            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)    

