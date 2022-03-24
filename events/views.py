from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from events.serializers import EventSerializer

# Create your views here.

class CreateEventAPIView(CreateAPIView):
    serializer_class=EventSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)
        