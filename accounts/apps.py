from django.apps import AppConfig
from django.db.models.signals import post_migrate


def seed_cebu_barangays(sender, **kwargs):
    from .models import Location
    default_barangays = [
        'Apas', 'Banilad', 'Basak San Nicolas', 'Busay', 'Capitol Site',
        'Guadalupe', 'Kasambagan', 'Labangon', 'Lahug', 'Mabolo',
        'Pardo', 'Punta Princesa', 'Sambag I', 'Sambag II', 'Talamban', 'Tisa'
    ]
    for brgy in default_barangays:
        Location.objects.get_or_create(
            barangay_name=brgy,
            defaults={'city': 'Cebu City'}
        )


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(seed_cebu_barangays, sender=self)