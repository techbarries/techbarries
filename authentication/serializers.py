from dataclasses import fields
import imp
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','first_name','last_name','profile_picture_url','is_active','phone_number','username','email')
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
          
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','first_name','last_name','profile_picture_url','is_active','phone_number','username','email')