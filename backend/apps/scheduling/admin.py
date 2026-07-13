from django.contrib import admin
from .models import Availability, Event, BookingRequest


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('videomaker', 'day_of_week', 'start_time', 'end_time', 'is_available')
    list_filter = ('day_of_week', 'is_available')
    raw_id_fields = ('videomaker',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'videomaker', 'client', 'event_type', 'status', 'start_datetime')
    list_filter = ('status', 'event_type')
    search_fields = ('title', 'videomaker__email', 'client__email')
    raw_id_fields = ('videomaker', 'client')


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'videomaker', 'event_type', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'event_type')
    raw_id_fields = ('client', 'videomaker')
