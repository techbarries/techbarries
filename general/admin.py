from django.contrib import admin
from general.models import Faq, Notification 
# Register your models here.

admin.site.register(Notification)
admin.site.register(Faq)