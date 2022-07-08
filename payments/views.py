from decouple import config
from django.shortcuts import render
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class CreateEventTransactionAPIView(APIView):
    """event_id, user_id, transaction_id, payment_status, bottle_fee, cover_fee, no_of_tickets, processing_fee, pulse_service_charges
    {
    "transaction_id": "pi_3LJLskFHPjA97y331KajVLja",
    "event_id":1,
    "user_id":2,
    "payment_status":true,
    "bottle_fee":20,
    "cover_fee":12,
    "no_of_tickets":1,
    "processing_fee":10,
    "pulse_service_charges":20
    
}"""
    serializer_class=EventTransactionSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        res={"status":True,"message":"Event transaction created successfully","data":{}}
        if serializer.is_valid():
            serializer.save()
            res.update(data=serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        res.update(status=False,message="Validation error",data={"errors":serializer.errors})    
        return Response(res,status=status.HTTP_200_OK)    

