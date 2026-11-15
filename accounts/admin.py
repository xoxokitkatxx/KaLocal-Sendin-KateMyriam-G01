from django.contrib import admin
from .models import Location, UserProfile


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'barangay_name', 'city')
    search_fields = ('barangay_name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'full_name', 'email', 'role', 'location', 'contact_number', 'created_at')
    list_filter = ('role', 'location')
    search_fields = ('full_name', 'email', 'contact_number')