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
    university_picture=models.ImageField(upload_to="university",blank=True,)
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
    image = models.ImageField(upload_to="venue",blank=True)
class Event(TrackingModel):
    class AccessType(models.TextChoices):
        PUBLIC = 'PUBLIC', ('PUBLIC')
        PRIVATE = 'PRIVATE', ('PRIVATE')
    name=models.CharField(max_length=255)
    coverPhoto=models.ImageField(upload_to="event_cover",blank=True)
    description=models.TextField(blank=True)
    address=models.CharField(max_length=255,blank=True)
    event_address_unit=models.CharField(max_length=255,blank=True)
    event_start_date=models.DateField(blank=True)
    event_end_date=models.DateField(blank=True)
    event_start_time=models.TimeField(blank=True)
    event_end_time=models.TimeField(blank=True)
    guests=models.ManyToManyField(to=User)
    university_campus=models.OneToOneField(to=University,on_delete=models.CASCADE,related_name="university_campus")
    venue=models.OneToOneField(to=Venue,on_delete=models.CASCADE,related_name="event_venue_name")
    access_type=models.CharField(max_length=10,choices=AccessType.choices,default=AccessType.PUBLIC)   
    guests_list_capacity=models.IntegerField(default=0,blank=True)
    open_guests_list=models.IntegerField(default=0,blank=True)
    contact_info=models.TextField(blank=True)
    cover_fee=models.PositiveIntegerField(default=0)
    bottle_service_fee=models.PositiveIntegerField(default=0)
    boost_enabled=models.BooleanField(default=0,blank=True)
    created_by=models.ForeignKey(to=User,related_name="created_by_user_event",blank=True,null=True,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='event_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event",blank=True)