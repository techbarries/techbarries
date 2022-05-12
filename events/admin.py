from django.contrib import admin

from events.models import Age, Dress, Event, EventImage, Food, Music, University, Venue, VenueImage

# Register your models here.
class VenueImageInline(admin.TabularInline):
    model = VenueImage
    extra = 3
class VenueAdmin(admin.ModelAdmin):
    inlines = [ VenueImageInline, ]
class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3
class EventAdmin(admin.ModelAdmin):
    inlines = [ EventImageInline, ]
admin.site.register(University)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Dress)
admin.site.register(Food)
admin.site.register(Music)
admin.site.register(Age)
