import email
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import SelectMultiple, TimeInput
from authentication.models import User
from events.models import Age, Dress, Event, EventImage, EventStatus, Food, MenuImage, Music, RequestVenue, University, Venue, VenueImage
from events.serializers import EventSerializer
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class VenueImageInline(admin.TabularInline):
    model = VenueImage
    readonly_fields = ('image_preview',)
    extra = 1
    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="50" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'
class VenueMenuImageInline(admin.TabularInline):
    model = MenuImage
    readonly_fields = ('image_preview',)
    extra = 1
    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="50" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'     
class VenueAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [ VenueMenuImageInline,VenueImageInline, ]
    exclude=('address','latitude','longitude')
    def save_model(self, request, obj, form, change):
        try:
            obj.address = obj.location.place
            obj.latitude = obj.location.latitude
            obj.longitude = obj.location.longitude
        except:
            pass    
        super().save_model(request, obj, form, change)

    def showLintScore(self,obj):
        lint_score=0
        events=Event.objects.filter(venue=obj.id,archived=True).all()
        if events.count() > 0:
            serializer = EventSerializer(events, many=True)
            for event in serializer.data:
                eventStatus=EventStatus.objects.filter(event_id=event['id']).all()    
                if eventStatus.count() > 0:
                    for eventStatusItem in eventStatus:
                        if eventStatusItem.checked_in:
                            lint_score+=6
                        if eventStatusItem.pinned:
                            lint_score+=5
                        if eventStatusItem.paid:
                            lint_score+=4
                        if eventStatusItem.guest_list:
                            lint_score+=3
                        if eventStatusItem.invited:
                            lint_score+=2

        return lint_score

    showLintScore.short_description="Lit Score"
    showLintScore.allow_tags = True
    def has_delete_permission(self, request, obj=None):
        return False     
    list_display=("venue_name","description","address","created_at","showLintScore",)
    search_fields = ['venue_name','description','address','created_at']
    fieldsets=[
        (
           "Basic Info",{
               'fields':('venue_name','description','location','price_details','featured','premium','popular')
           } 
        ),
        (
           "Attractions",{
               'classes':('collapse',),
               'fields':('dresses','foods','musics','ages')
           } 
        ),
        (
           "Bussiness Hours",{
               'classes':('collapse',),
               'fields':
               ('monday',('monday_start_time','monday_end_time')
               ,'tuesday',('tuesday_start_time','tuesday_end_time')
               ,'wednesday',('wednesday_start_time','wednesday_end_time')
               ,'thursday',('thursday_start_time','thursday_end_time')
               ,'friday',('friday_start_time','friday_end_time')
               ,'saturday',('saturday_start_time','saturday_end_time')
               ,'sunday',('sunday_start_time','sunday_end_time'))
           } 
        ),
        (
           "Contact Info",{
               'classes':('collapse',),
               'fields':('email','phone','promoter_user','created_by','archived')
           } 
        ),
    ]
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'style':'min-width:250px;min-height:80px'})},models.TimeField:{'widget':TimeInput(attrs={'size':'20'})}, }

            
class EventImageInline(admin.TabularInline):
    model = EventImage
    readonly_fields = ('image_preview',)
    extra = 1
    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="50" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'    
class EventAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    inlines = [ EventImageInline, ]
    def has_delete_permission(self, request, obj=None):
        return False     
    list_display=("name","description","address","venue","boost_enabled","created_at",)
    search_fields = ['name','description','address','created_at']
class UniversityAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False     
    list_display=("university_name","city","archived","created_at",)
    search_fields = ['university_name','city','archived','created_at']

class RequestVenueAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False  
    def getEmail(self,obj):
        user=User.objects.filter(email=obj.user_id).first()    
        return user.email
    def getPhone(self,obj):
        user=User.objects.filter(email=obj.user_id).first()    
        return user.phone_number  
    getEmail.short_description="Email"      
    getPhone.short_description="Phone"      
    list_display=("name","city","getEmail","getPhone","created_at",)
    search_fields = ['name','city','user_id__email','user_id__phone_number','created_at']

admin.site.register(University,UniversityAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(RequestVenue,RequestVenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Dress)
admin.site.register(Food)
admin.site.register(Music)
admin.site.register(Age)
