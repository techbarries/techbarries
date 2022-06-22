from decouple import config
from django.shortcuts import render
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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