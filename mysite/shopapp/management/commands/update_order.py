from django.contrib.auth.models import User
from django.core.management import BaseCommand

from mysite.shopapp import Product, Order


class Command(BaseCommand):
    """Update order"""

    def handle(self, *args, **options):
        self.stdout.write("Create order")
        order = Order.objects.first()
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added product {order.products.all()} to order {order}"
            )
        )
