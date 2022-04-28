from dataclasses import fields
from unittest.util import _MAX_LENGTH
from rest_framework import serializers

from general.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields='__all__'
