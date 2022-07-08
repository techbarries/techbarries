from django.urls import path
from payments.views import CreatePaymentIntentAPIView,CreateEventTransactionAPIView

urlpatterns=[
    path('create',CreatePaymentIntentAPIView.as_view(),name="payment-intent"),
    path('event/create',CreateEventTransactionAPIView.as_view(),name="event-transaction"),
]