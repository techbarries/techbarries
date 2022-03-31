from django.contrib import admin
from authentication.models import Device, User

# Register your models here.

admin.site.register(User)
admin.site.register(Device)
