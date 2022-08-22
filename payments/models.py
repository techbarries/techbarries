from django.db import models
from authentication.models import User
from events.models import Event

from helpers.models import TrackingModel

# Create your models here.
class EventTransaction(TrackingModel):
    event_id = models.ForeignKey(Event, related_name='event_transaction',on_delete=models.CASCADE)
    user_id=models.ForeignKey(to=User,related_name="user_event_transaction",on_delete=models.CASCADE)
    transaction_id=models.TextField()
    payment_status = models.BooleanField(("Is Paid"),default=False,help_text=("Designates whether the payment is successfull."),blank=True)
    bottle_fee=models.IntegerField(default=0,blank=True,null=True)
    payment_method=models.CharField(max_length=255,blank=True,null=True)
    currency=models.CharField(max_length=255,blank=True,null=True)
    cover_fee=models.IntegerField(default=0,blank=True,null=True)
    no_of_tickets=models.IntegerField(default=1,blank=True,null=True)
    processing_fee=models.IntegerField(default=0,blank=True,null=True)
    service_tip=models.IntegerField(default=0,blank=True,null=True)
    pulse_service_charges=models.IntegerField(default=0,blank=True,null=True)


