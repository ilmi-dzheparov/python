from typing import Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Create order"""

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="admin")
        products: Sequence[Product] = Product.objects.only("id", "name").all()
        order, created = Order.objects.get_or_create(
            delivery_address="ul/ Pupkina, d.8",
            promocode="SALE11",
            user=user,
        )
        for product in products:
            order.products.add(product)
        order.save()

        self.stdout.write(self.style.SUCCESS(f"Created order {order}"))
