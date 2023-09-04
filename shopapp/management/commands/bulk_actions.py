from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Create order"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")
        # info = [
        #     ('NoPhone 1', 199, 1),
        #     ('NoPhone 2', 299, 1),
        #     ('NoPhone 3', 399, 1),
        # ]
        # products = [
        #     Product(name=name, price=price, created_by_id=id)
        #     for name, price, id in info
        # ]
        res = Product.objects.filter(name__contains="NoPhone").update(description='very nice phone, must buy')
        print(res)
        # for obj in res:
        #     print(obj)

        self.stdout.write('Done')