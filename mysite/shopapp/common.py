from csv import DictReader
from io import TextIOWrapper

from shopapp.models import Product, Order


def save_csv_products(file, encoding):
# admin.site.register(Product, ProductAdmin)
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
                             )
    reader = DictReader(csv_file)

    products = [
        Product(**row)
        for row in reader
    ]

    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding):
# admin.site.register(Product, ProductAdmin)
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
                             )
    reader = DictReader(csv_file)
    orders = list
    for row in reader:
        print(row)
        print(row["products"].split(','))
        products = [
            Product.objects.get(pk=product_id)
            for product_id in row["products"].split(',')
        ]
        order = Order.objects.create(
            delivery_address=row["delivery_address"],
            promocode=row["promocode"],
            user_id=row["user_id"],
        )
        order.products.set(products)
        print(order)

    return order

