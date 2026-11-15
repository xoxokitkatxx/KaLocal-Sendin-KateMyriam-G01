import django
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


def make_check_constraint(q_obj, name):
    """Supports CheckConstraint across Django 5.0 and 5.1+/6.0."""
    if django.VERSION >= (5, 1):
        return models.CheckConstraint(condition=q_obj, name=name)
    return models.CheckConstraint(check=q_obj, name=name)


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    barangay_name = models.CharField(max_length=100, unique=True)  # BR-08
    city = models.CharField(max_length=100, default='Cebu City')

    class Meta:
        db_table = 'locations'
        ordering = ['barangay_name']

    def __str__(self):
        return f"{self.barangay_name}, {self.city}"


class UserProfile(models.Model):
    ROLE_VENDOR = 'VENDOR'
    ROLE_CONSUMER = 'CONSUMER'

    ROLE_CHOICES = [
        (ROLE_VENDOR, 'Local Vendor / Merchant'),
        (ROLE_CONSUMER, 'Consumer'),
    ]

    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        db_column='location_id',
        related_name='users'
    )  # BR-03
    email = models.EmailField(max_length=150, unique=True)  # BR-01
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)  # BR-02
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profiles'
        constraints = [
            make_check_constraint(
                Q(role__in=['VENDOR', 'CONSUMER']),
                name='check_valid_user_role'
            )
        ]

    def __str__(self):
        return f"{self.full_name} ({self.role}) - {self.location.barangay_name}"