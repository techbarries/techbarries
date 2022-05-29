from django.contrib import admin
from django.utils.safestring import mark_safe
from events.models import Age, Dress, Event, EventImage, Food, Music, University, Venue, VenueImage

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
class VenueAdmin(admin.ModelAdmin):
    inlines = [ VenueImageInline, ]
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
