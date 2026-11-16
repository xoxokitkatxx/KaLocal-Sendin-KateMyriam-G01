from django.test import TestCase
from django.contrib.auth.models import User
from uuid import uuid4

from .models import Location, Product, UserProfile


class DashboardTests(TestCase):
    def setUp(self):
        self.suffix = uuid4().hex
        self.home_location = Location.objects.create(
            barangay_name=f'Apas-{self.suffix}',
            city='Cebu City',
        )
        self.other_location = Location.objects.create(
            barangay_name=f'Lahug-{self.suffix}',
            city='Cebu City',
        )

    def create_profile(self, username, role, location):
        username = f'{username}-{self.suffix}'
        user = User.objects.create_user(username=username, password='test-password')
        profile = UserProfile.objects.create(
            user=user,
            full_name=username.title(),
            email=f'{username}@example.com',
            role=role,
            location=location,
        )
        return user, profile

    def create_product(self, vendor, name, is_active=True):
        return Product.objects.create(
            vendor=vendor,
            name=name,
            price='10.00',
            is_active=is_active,
        )

    def test_vendor_dashboard_shows_only_own_products(self):
        vendor_user, vendor = self.create_profile(
            'vendor',
            UserProfile.ROLE_VENDOR,
            self.home_location,
        )
        _, other_vendor = self.create_profile(
            'other-vendor',
            UserProfile.ROLE_VENDOR,
            self.home_location,
        )
        self.create_product(vendor, 'My product')
        self.create_product(other_vendor, 'Other product')
        self.create_product(vendor, 'Inactive product', is_active=False)

        self.client.force_login(vendor_user)
        response = self.client.get('/accounts/dashboard/')

        self.assertContains(response, 'My product')
        self.assertContains(response, 'Inactive product')
        self.assertNotContains(response, 'Other product')
        self.assertEqual(response.context['active_products_count'], 1)

    def test_consumer_can_filter_active_products_by_location(self):
        consumer_user, _ = self.create_profile(
            'consumer',
            UserProfile.ROLE_CONSUMER,
            self.home_location,
        )
        _, home_vendor = self.create_profile(
            'home-vendor',
            UserProfile.ROLE_VENDOR,
            self.home_location,
        )
        _, other_vendor = self.create_profile(
            'other-vendor',
            UserProfile.ROLE_VENDOR,
            self.other_location,
        )
        self.create_product(home_vendor, 'Apas product')
        self.create_product(other_vendor, 'Lahug product')
        self.create_product(other_vendor, 'Inactive Lahug product', is_active=False)

        self.client.force_login(consumer_user)
        response = self.client.get(
            '/accounts/dashboard/',
            {'location': self.other_location.pk},
        )

        self.assertContains(response, 'Lahug product')
        self.assertNotContains(response, 'Apas product')
        self.assertNotContains(response, 'Inactive Lahug product')
        self.assertEqual(response.context['selected_location'], self.other_location)
