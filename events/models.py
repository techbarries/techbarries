from datetime import datetime
import imp
from django.db import models
from helpers.models import TrackingModel
from authentication.models import User
from places.fields import PlacesField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class University(TrackingModel):
    university_name=models.CharField(max_length=255)
    city=models.CharField(max_length=255,blank=True)
    state=models.CharField(max_length=255,blank=True)
    country=models.CharField(max_length=255,blank=True)
    university_picture=models.ImageField(upload_to="university/%Y/%m/%d/",blank=True,)
    created_by=models.ForeignKey(to=User,related_name="created_by_user_uni",blank=True,null=True,default=None,on_delete=models.CASCADE)
    archived = models.BooleanField(
        ("Archived"),
        default=False,
        help_text=("Designates whether the university is archived or not."),
        blank=True
    )
    class  Meta:  #new
        verbose_name_plural  =  "Universities"
    def __str__(self):
        return self.university_name
class Dress(TrackingModel):
    dress_name=models.CharField(max_length=255)
    created_by=models.ForeignKey(to=User,related_name="dress_created_by_user",blank=True,null=True,default=None,on_delete=models.CASCADE)
    def __str__(self):
        return self.dress_name

class Food(TrackingModel):
    food_name=models.CharField(max_length=255)
    created_by=models.ForeignKey(to=User,related_name="food_created_by_user",blank=True,null=True,default=None,on_delete=models.CASCADE)
    def __str__(self):
        return self.food_name

class Music(TrackingModel):
    music_name=models.CharField(max_length=255)
    created_by=models.ForeignKey(to=User,related_name="music_created_by_user",blank=True,null=True,default=None,on_delete=models.CASCADE)
    def __str__(self):
        return self.music_name

class Age(TrackingModel):
    age_name=models.CharField(max_length=255)
    created_by=models.ForeignKey(to=User,related_name="age_created_by_user",blank=True,null=True,default=None,on_delete=models.CASCADE)
    def __str__(self):
        return self.age_name        
class Venue(TrackingModel):
    class PriceType(models.TextChoices):
        Single = '$', ('$')
        Double = '$$', ('$$')
        Triple = '$$$', ('$$$')
    venue_name=models.CharField(max_length=255)
    description=models.TextField(max_length=1000,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    latitude=models.CharField(max_length=255,blank=True,null=True)
    longitude=models.CharField(max_length=255,blank=True,null=True)
    location = PlacesField(null=True,blank=True)
    price_details=models.CharField(("Price Details"),max_length=10,choices=PriceType.choices,default=PriceType.Single,null=True)   
    
    
    dresses=models.ManyToManyField(to=Dress,blank=True)
    foods=models.ManyToManyField(to=Food,blank=True)
    musics=models.ManyToManyField(to=Music,blank=True)
    ages=models.ManyToManyField(to=Age,blank=True)
    
    featured = models.BooleanField(
        ("Featured"),
        default=False,
        help_text=("Designates whether the venue is featured or not."),
        blank=True
    )
    premium = models.BooleanField(
        ("Premium"),
        default=False,
        help_text=("Designates whether the venue is premium or not."),
        blank=True
    )
    popular = models.BooleanField(
        ("popular"),
        default=False,
        help_text=("Designates whether the venue is popular or not."),
        blank=True
    )    
    monday = models.BooleanField(default=True,blank=True)
    monday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    monday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    tuesday = models.BooleanField(default=True,blank=True)
    tuesday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    tuesday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    wednesday = models.BooleanField(default=True,blank=True)
    wednesday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    wednesday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    thursday = models.BooleanField(default=True,blank=True)
    thursday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    thursday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    friday = models.BooleanField(default=True,blank=True)
    friday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    friday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    saturday = models.BooleanField(default=True,blank=True)
    saturday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    saturday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    sunday = models.BooleanField(default=True,blank=True)
    sunday_start_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")
    sunday_end_time=models.TimeField(blank=True,null=True,default=datetime.now,help_text="Enter Time")

    email=models.EmailField(max_length=255,blank=True,null=True)
    phone=PhoneNumberField(blank=True,null=True)
    promoter_user=models.ForeignKey(to=User,related_name="promoter_user_venue",blank=True,null=True,default=None,on_delete=models.CASCADE)
    created_by=models.ForeignKey(to=User,related_name="created_by_user_venue",blank=True,null=True,default=None,on_delete=models.CASCADE)
    archived = models.BooleanField(
        ("Archived"),
        default=False,
        help_text=("Designates whether the venue is archived or not."),
        blank=True
    )
    def __str__(self):
        return self.venue_name
        
class MenuImage(models.Model):
    class ImageType(models.TextChoices):
        Yes = True, ('Yes')
        No = False, ('No')
    venue = models.ForeignKey(Venue, related_name='venue_menu_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="menu/%Y/%m/%d-%h:%i/",blank=True) 
    is_cover=models.CharField(max_length=10,choices=ImageType.choices,default=ImageType.No,null=True)   


class VenueImage(models.Model):
    class ImageType(models.TextChoices):
        Yes = True, ('Yes')
        No = False, ('No')
    venue = models.ForeignKey(Venue, related_name='venue_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="venue/%Y/%m/%d/",blank=True)
    is_cover=models.CharField(max_length=10,choices=ImageType.choices,default=ImageType.No,null=True)   


class RequestVenue(TrackingModel,models.Model):
    name=models.CharField(max_length=255)
    city=models.CharField(max_length=255,blank=True,null=True)
    user_id=models.ForeignKey(to=User,related_name="user_requested_venue",blank=True,null=True,default=None,on_delete=models.CASCADE)
    class  Meta:  #new
        verbose_name_plural  =  "Requested Venues"
    def __str__(self):
        return self.name      

class Event(TrackingModel):
    class AccessType(models.TextChoices):
        PUBLIC = 'PUBLIC', ('PUBLIC')
        PRIVATE = 'PRIVATE', ('PRIVATE')
    name=models.CharField(max_length=255)
    cover_photo=models.ImageField(upload_to="event_cover/%Y/%m/%d/",blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    latitude=models.FloatField(max_length=255,blank=True,null=True)
    longitude=models.FloatField(max_length=255,blank=True,null=True)
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
    boost_enabled = models.BooleanField(("Boost enabled"),default=False,help_text=("Designates whether the event can boost."),blank=True)
    archived = models.BooleanField(
        ("Archived"),
        default=False,
        help_text=("Designates whether the event is archived or not."),
        blank=True
    )
    user_id=models.ForeignKey(to=User,related_name="user_created_event",blank=True,null=True,default=None,on_delete=models.CASCADE)
    created_by=models.ForeignKey(to=User,related_name="created_by_event_user",blank=True,null=True,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
        
class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='event_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event/%Y/%m/%d/",blank=True)

    def __str__(self):
        return self.event.name

class EventStatus(TrackingModel,models.Model):
    event_id = models.ForeignKey(Event, related_name='event_status',on_delete=models.CASCADE)
    user_id=models.ForeignKey(to=User,related_name="user_event_interaction",blank=True,null=True,default=None,on_delete=models.CASCADE)
    hosted=models.BooleanField(default=0,blank=True,null=True)
    checked_in=models.BooleanField(default=0,blank=True,null=True)
    pinned=models.BooleanField(default=0,blank=True,null=True)
    paid=models.BooleanField(default=0,blank=True,null=True)
    guest_list=models.BooleanField(default=0,blank=True,null=True)
    invited=models.BooleanField(default=0,blank=True,null=True)
    joined=models.BooleanField(default=0,blank=True,null=True)
    going=models.BooleanField(default=0,blank=True,null=True)
    liked=models.BooleanField(default=0,blank=True,null=True)
    public=models.BooleanField(default=0,blank=True,null=True)
    not_going=models.BooleanField(default=0,blank=True,null=True)

class VenueStatus(TrackingModel,models.Model):
    venue_id = models.ForeignKey(Venue, related_name='venue_status',on_delete=models.CASCADE)
    user_id=models.ForeignKey(to=User,related_name="user_venue_interaction",blank=True,null=True,default=None,on_delete=models.CASCADE)
    liked=models.BooleanField(default=0,blank=True,null=True)
    joined=models.BooleanField(default=0,blank=True,null=True)