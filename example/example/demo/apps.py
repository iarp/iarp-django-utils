import random

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def setup_dummy_data(sender, **kwargs):
    from .models import Item

    print('Generating Dummy Data')

    for x in range(100):
        item, _ = Item.objects.get_or_create(body=f'Item {x}')
        for k in range(random.randint(15, 60)):
            item.subitems.get_or_create(body=f"Item {x} - SubItem {k}")


class DemoConfig(AppConfig):
    name = 'example.demo'

    def ready(self):
        post_migrate.connect(setup_dummy_data, sender=self)
