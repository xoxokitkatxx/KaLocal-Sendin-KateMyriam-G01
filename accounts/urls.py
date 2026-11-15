from django.contrib import admin
from django.urls import path, include  # Add 'include' to this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Connect your accounts app URLs
]