
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models import Avg, Min, Max, Sum, Count

from shopapp.models import Product, Order


class Command(BaseCommand):
    """Create order"""

    def handle(self, *args, **options):
        self.stdout.write("Start demo aggregate")

        # result = Product.objects.aggregate(
        #     Avg("price"),
        #     Max("price"),
        #     min_price=Min("price"),
        #     count=Count("id"),
        # )
        # result_2 = Product.objects.filter(
        #     name__contains="NoPhone",
        # ).aggregate(
        #     Avg("price"),
        #     Max("price"),
        #     min_price=Min("price"),
        #     count=Count("id"),
        # )
        # print(result)
        # print((result_2))

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0),
            products_count=Count('products')
        )
        for order in orders:
            print(
                f"Order #{order.id} "
                f"with {order.products_count} "
                f"products worth {order.total}"
            )

        self.stdout.write('Done')