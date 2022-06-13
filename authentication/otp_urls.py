from authentication.views import GenerateSmsOTP ,VerifySmsOTP
from django.urls import path

urlpatterns=[
    path('send/<str:phone>',GenerateSmsOTP.as_view(),name="sms_otp"),
    path('verify/<str:phone>/otp/<int:otp>',VerifySmsOTP.as_view(),name="sms_otp")
]