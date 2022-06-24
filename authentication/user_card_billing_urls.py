from authentication.views import CardBillingListAPIView,CreateCardBillingAPIView 
from django.urls import path

urlpatterns=[
    path('create',CreateCardBillingAPIView.as_view(),name="card-billing-create"),
    path('list/user/<int:user_id>/otp/<int:otp>',CardBillingListAPIView.as_view(),name="card-billing")
]