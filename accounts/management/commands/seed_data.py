from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from accounts.models import Location, UserProfile, Product


class Command(BaseCommand):
    help = 'Seeds 3 mock products for every available Location (Barangay) in the database.'

    def handle(self, *args, **kwargs):
        locations = Location.objects.all()

        if not locations.exists():
            self.stdout.write(self.style.ERROR(
                "No locations found in the database! Please add barangays first."
            ))
            return

        # Pool of realistic Cebuano products to rotate across barangays
        product_pool = [
            [
                {'name': 'Homemade Cebu Longganisa (Dozen)', 'price': 180.00, 'category': 'FOOD', 'desc': 'Sweet and garlicky native pork sausages made fresh daily.'},
                {'name': 'Fresh Ripe Mangoes (1kg)', 'price': 130.00, 'category': 'PRODUCE', 'desc': 'Sweet export-quality Cebu mangoes.'},
                {'name': 'Purified Water Refill (1 Gallon)', 'price': 35.00, 'category': 'GROCERY', 'desc': 'Round or slim container. Free delivery within the barangay.'},
            ],
            [
                {'name': 'Cebu Lechon Belly (1kg)', 'price': 850.00, 'category': 'FOOD', 'desc': 'Crispy skin, juicy meat stuffed with lemongrass and spices.'},
                {'name': 'Farm-Fresh Highland Vegetables Bundle', 'price': 160.00, 'category': 'PRODUCE', 'desc': 'Cabbage, carrots, and chayote sourced directly from Busay farmers.'},
                {'name': 'Aircon Cleaning & Checkup', 'price': 750.00, 'category': 'SERVICES', 'desc': 'Thorough cleaning for window-type and split-type units.'},
            ],
            [
                {'name': 'Danggit & Pusit Pack (250g)', 'price': 250.00, 'category': 'FOOD', 'desc': 'Crispy dried fish and squid sourced from Taboan Market.'},
                {'name': 'Sari-Sari Breakfast Bundle', 'price': 195.00, 'category': 'GROCERY', 'desc': 'Includes 1 tray of medium eggs, pandesal pack, and tablea.'},
                {'name': 'Home Plumbing & Faucet Repair', 'price': 450.00, 'category': 'SERVICES', 'desc': 'Quick neighborhood repair for leaks, pipes, and sink fixtures.'},
            ],
            [
                {'name': 'Puso / Hanging Rice (Pack of 10)', 'price': 80.00, 'category': 'FOOD', 'desc': 'Freshly boiled woven coconut-leaf rice, perfect with barbecue.'},
                {'name': 'Sikwate & Putomaya Merienda Set', 'price': 120.00, 'category': 'FOOD', 'desc': 'Warm sticky rice with ginger paired with rich Cebuano hot chocolate.'},
                {'name': 'Laundry Wash, Dry & Fold (per 5kg)', 'price': 175.00, 'category': 'SERVICES', 'desc': 'Same-day neighborhood laundry service with free fabric conditioner.'},
            ],
        ]

        store_prefixes = [
            "Nanay Maria's Hub",
            "Kuya Ben's Trading",
            "Tindahan sa Barangay",
            "Cebu Lokal Merkado",
        ]

        total_created = 0

        for index, location in enumerate(locations):
            # 1. Check if this barangay already has a Vendor; if not, create one
            vendor = UserProfile.objects.filter(role=UserProfile.ROLE_VENDOR, location=location).first()

            if not vendor:
                slug = slugify(location.barangay_name).replace('-', '_')[:30]
                username = f"vendor_{slug}"
                email = f"{username}@kalocal.ph"
                store_name = f"{store_prefixes[index % len(store_prefixes)]} ({location.barangay_name})"

                user, created_user = User.objects.get_or_create(
                    username=username,
                    defaults={'email': email}
                )
                if created_user:
                    user.set_password('KalocalVendor123!')
                    user.save()

                vendor, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'full_name': store_name,
                        'email': email,
                        'role': UserProfile.ROLE_VENDOR,
                        'location': location,
                        'contact_number': f"0917{1000000 + index:07d}",
                        'bio': f"Trusted local vendor serving residents of {location.barangay_name}, {location.city}.",
                    }
                )

            # 2. Pick a set of 3 products for this barangay
            products_for_barangay = product_pool[index % len(product_pool)]

            for item in products_for_barangay:
                _, created_prod = Product.objects.get_or_create(
                    vendor=vendor,
                    name=item['name'],
                    defaults={
                        'price': item['price'],
                        'category': item['category'],
                        'description': item['desc'],
                        'is_active': True,
                    }
                )
                if created_prod:
                    total_created += 1

            self.stdout.write(self.style.SUCCESS(
                f"✔ {location.barangay_name}: Ensured 3 products under store '{vendor.full_name}'"
            ))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Added {total_created} new products across {locations.count()} barangays."
        ))