import imp
from telnetlib import STATUS
from urllib import response
from django.shortcuts import render
from rest_framework.generics import GenericAPIView,CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView
from authentication.models import Device, User
from authentication.serializers import DeviceSerializer, PulseUserSerializer, UserSerializer
from rest_framework import response,status
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class RegisterAPIView(GenericAPIView):
    serializer_class=PulseUserSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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

class UserByTokenView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'user_token'
    def get_queryset(self):
        user_token = self.request.parser_context['kwargs'].get('user_token')
        return User.objects.all().filter(user_token=user_token)
