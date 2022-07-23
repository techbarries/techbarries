from django.contrib import admin
from general.models import Faq, Notification, Report 
# Register your models here.

admin.site.register(Notification)
admin.site.register(Faq)
admin.site.register(Report)