import imp
from operator import mod
from os import access
from pyexpat import model
from unicodedata import name
from django.db import models
from helpers.models import TrackingModel
from authentication.models import User
# Create your models here.

class University(TrackingModel):
    university_name=models.CharField(max_length=255)
    city=models.CharField(max_length=255,blank=True)
    state=models.CharField(max_length=255,blank=True)
    country=models.CharField(max_length=255,blank=True)
    university_picture=models.ImageField(upload_to="university/%Y/%m/%d/",blank=True,)
    created_by=models.ForeignKey(to=User,related_name="created_by_user_uni",blank=True,null=True,default=None,on_delete=models.CASCADE)
    class  Meta:  #new
        verbose_name_plural  =  "Universities"
    def __str__(self):
        return self.university_name
class Venue(TrackingModel):
    venue_name=models.CharField(max_length=255)
    created_by=models.ForeignKey(to=User,related_name="created_by_user_venue",blank=True,null=True,default=None,on_delete=models.CASCADE)
    def __str__(self):
        return self.venue_name
class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, related_name='venue_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="venue/%Y/%m/%d/",blank=True)
class Event(TrackingModel):
    class AccessType(models.TextChoices):
        PUBLIC = 'PUBLIC', ('PUBLIC')
        PRIVATE = 'PRIVATE', ('PRIVATE')
    name=models.CharField(max_length=255)
    cover_photo=models.ImageField(upload_to="event_cover/%Y/%m/%d/",blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    event_address_unit=models.CharField(max_length=255,blank=True,null=True)
    event_start_date=models.DateField(blank=True,null=True)
    event_end_date=models.DateField(blank=True,null=True)
    event_start_time=models.TimeField(blank=True,null=True)
    event_end_time=models.TimeField(blank=True,null=True)
    guests=models.ManyToManyField(to=User)
    university_campus=models.ForeignKey(to=University,on_delete=models.CASCADE,related_name="university_campus",null=True,blank=True)
    venue=models.ForeignKey(to=Venue,on_delete=models.CASCADE,related_name="event_venue_name",null=True,blank=True)
    access_type=models.CharField(max_length=10,choices=AccessType.choices,default=AccessType.PUBLIC,null=True)   
    guests_list_capacity=models.IntegerField(default=0,blank=True,null=True)
    open_guests_list=models.IntegerField(default=0,blank=True,null=True)
    contact_info=models.TextField(blank=True,null=True)
    cover_fee=models.PositiveIntegerField(default=0,null=True)
    bottle_service_fee=models.PositiveIntegerField(default=0,null=True)
    boost_enabled=models.BooleanField(default=0,blank=True,null=True)
    user_id=models.ForeignKey(to=User,related_name="user_created_event",blank=True,null=True,default=None,on_delete=models.CASCADE)
    created_by=models.ForeignKey(to=User,related_name="created_by_event_user",blank=True,null=True,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='event_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event/%Y/%m/%d/",blank=True)