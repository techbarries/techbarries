from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import SelectMultiple

from events.models import Age, Dress, Event, EventImage, EventStatus, Food, MenuImage, Music, University, Venue, VenueImage
from events.serializers import EventSerializer

# Register your models here.
class VenueImageInline(admin.TabularInline):
    model = VenueImage
    readonly_fields = ('image_preview',)
    extra = 3
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
    extra = 3
    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="50" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'     
class VenueAdmin(admin.ModelAdmin):
    inlines = [ VenueMenuImageInline,VenueImageInline, ]
    exclude=('address','latitude','longitude')
    formfield_overrides = { models.ManyToManyField: {'widget': SelectMultiple(attrs={'style':'min-width:250px'})}, }
    def save_model(self, request, obj, form, change):
        obj.address = obj.location.place
        obj.latitude = obj.location.latitude
        obj.longitude = obj.location.longitude
        super().save_model(request, obj, form, change)

    def showLintScore(self,obj):
        lint_score=0
        events=Event.objects.filter(venue=obj.id,status=True).all()
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

    showLintScore.short_description="Lint Score"
    showLintScore.allow_tags = True    
    list_display=("id","venue_name","showLintScore",)
            
class EventImageInline(admin.TabularInline):
    model = EventImage
    readonly_fields = ('image_preview',)
    extra = 3
    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="50" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'    
class EventAdmin(admin.ModelAdmin):
    inlines = [ EventImageInline, ]
admin.site.register(University)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Dress)
admin.site.register(Food)
admin.site.register(Music)
admin.site.register(Age)
