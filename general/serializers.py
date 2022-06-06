from dataclasses import fields
from unittest.util import _MAX_LENGTH
from rest_framework import serializers

from general.models import Friends, InviteFriends, Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields='__all__'
        
class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friends
        fields='__all__'

class InviteFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=InviteFriends
        fields='__all__'
