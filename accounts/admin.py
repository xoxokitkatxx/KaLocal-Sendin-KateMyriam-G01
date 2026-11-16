from django.contrib import admin
from .models import Location, UserProfile, Product

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('barangay_name', 'city')
    search_fields = ('barangay_name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'email', 'location')
    list_filter = ('role', 'location')
    search_fields = ('full_name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'category', 'is_active')
    list_filter = ('category', 'is_active', 'vendor__location')
    search_fields = ('name', 'vendor__full_name')