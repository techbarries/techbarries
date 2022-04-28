from authentication.views import DeviceAPIView,DeviceListAPIView,CreateDeviceAPIView 
from django.urls import path

urlpatterns=[
    path('',DeviceAPIView.as_view(),name="devices"),
    path('create',CreateDeviceAPIView.as_view(),name="device-create"),
    path('<int:user_id>',DeviceListAPIView.as_view(),name="device")
]