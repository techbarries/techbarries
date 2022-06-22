from django.urls import path
from payments.views import CreatePaymentIntentAPIView

urlpatterns=[
    path('create',CreatePaymentIntentAPIView.as_view(),name="payment-intent"),
]