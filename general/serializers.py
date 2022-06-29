from dataclasses import fields
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.serializers import UserSerializer

from general.models import Friends, InviteFriends, Notification

class NotificationSerializer(serializers.ModelSerializer):
    user_id=UserSerializer()
    created_by=UserSerializer()
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
