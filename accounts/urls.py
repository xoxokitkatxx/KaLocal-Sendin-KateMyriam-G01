from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard_redirect'),
    path('dashboard/vendor/', views.dashboard_view, name='vendor_dashboard'),
    path('dashboard/consumer/', views.dashboard_view, name='consumer_dashboard'),
    path('dashboard/vendor/product/add/', views.product_create_view, name='product_create'),
    path('dashboard/vendor/product/edit/<int:pk>/', views.product_update_view, name='product_update'),
    path('dashboard/vendor/product/delete/<int:pk>/', views.product_delete_view, name='product_delete'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_view, name='profile_edit'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
]