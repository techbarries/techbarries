from django.db import models
from authentication.models import User

from helpers.models import TrackingModel

# Create your models here.

class Notification(TrackingModel):
    class RedirectType(models.TextChoices):
        EVENT_PAGE = 'EVENT_PAGE', ('EVENT_PAGE')
        EVENT_GUEST_LIST_PAGE = 'EVENT_GUEST_LIST_PAGE', ('EVENT_GUEST_LIST_PAGE')
        CHAT_PAGE = 'CHAT_PAGE', ('CHAT_PAGE')
        FRIEND_PROFILE_PAGE = 'FRIEND_PROFILE_PAGE', ('FRIEND_PROFILE_PAGE')
        MY_WALLET_PAGE = 'MY_WALLET_PAGE', ('MY_WALLET_PAGE')
        MY_WALLET_TICKET_PAGE = 'MY_WALLET_TICKET_PAGE', ('MY_WALLET_TICKET_PAGE')
        REPORT_PAGE = 'REPORT_PAGE', ('REPORT_PAGE')
    title=models.CharField(max_length=255)
    description = models.TextField(("description"),default=None,null=True,blank=True)
    redirect_to=models.CharField(max_length=100,choices=RedirectType.choices,default=RedirectType.EVENT_PAGE,null=True)   
    details = models.TextField(("details"),default=None,null=True,blank=True)
    status=models.BooleanField(default=0,blank=True,null=True)
    user_id=models.ForeignKey(to=User,related_name="notification_user",blank=True,null=True,default=None,on_delete=models.CASCADE)
    created_by=models.ForeignKey(to=User,related_name="notification_created_by_user",blank=True,null=True,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
        