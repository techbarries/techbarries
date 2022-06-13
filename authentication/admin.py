from django.contrib import admin
from authentication.models import Device, SmsOTP, User
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False     
    list_display=("email","first_name","last_name","university","phone_number","created_at",)
    search_fields = ['first_name','last_name','university',"phone_number","email",'created_at']
    
admin.site.register(User,UserAdmin)
admin.site.register(Device)
admin.site.register(SmsOTP)
