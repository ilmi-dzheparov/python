from random import choices
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.shortcuts import reverse
from django.test import TestCase

from .models import Product, Order
from .utils import add_two_numbers

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2,3)
        self.assertEquals(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="qwerty")
        self.user.user_permissions.add(Permission.objects.get(codename='add_product'))
        self.client.force_login(self.user)

        self.product_name = "".join(choices(ascii_letters, k=7))
        # Generation of random product name
        Product.objects.filter(name=self.product_name).delete()
        # Deleting the product with such name

    def tearDown(self) -> None:
        # self.user.user_permissions.delete()
        Product.objects.filter(name=self.product_name).delete()
        self.user.delete()

    def test_create_product(self):

        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            })
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(username="test2", password="11111")
        cls.product = Product.objects.create(name="Best product", created_by_id = cls.user.pk)

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()


    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:products_detail",
                    kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check(self):
        response = self.client.get(
            reverse("shopapp:products_detail",
                    kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


# class ProductListViewTestCase(TestCase):
#     fixtures = [
#         "products-fixture.json",
#         "users-fixture.json",
#         "groups-fixture.json",
#     ]
#     def test_products(self):
#         response = self.client.get(reverse("shopapp:products_list"))
#         for product in Product.objects.filter(archived=False).all():
#             self.assertContains(response, product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
        "users-fixture.json",
        "groups-fixture.json",
    ]
    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bob", password="qwerty")
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Order")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsExportViewtestCase(TestCase):
    fixtures = [
        "products-fixture.json",
        "users-fixture.json",
        "groups-fixture.json",
    ]
    def test_get_products_view(self):
        response = self.client.get(reverse("shopapp:products_export"))
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(products_data["products"], expected_data)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="bob_test", password="qwerty")
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)
        self.order = Order.objects.create(
            user_id=self.user.pk,
            # delivery_address="test_adress",
            # promocode="test-promocode",
        )

    def tearDown(self) -> None:
        self.order.delete()


    def test_order_details_view(self):
        response = self.client.get(
            reverse(
                "shopapp:order_detail",
                kwargs={"pk": self.order.pk},
            )
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["order"].pk, self.order.pk)


class OrdersExportViewTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
        "orders-fixture.json",
        "users-fixture.json",
        "groups-fixture.json",
    ]
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username="rod_test", password="qwerty", is_staff=False)
        cls.user = User.objects.create_user(**cls.credentials)
        # cls.user.is_staff = True
        # cls.user.is_active = True
        # cls.user.user_permissions.add(Permission.objects.get(codename="view_order"))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.login(**self.credentials)

    def test_orders_export_view(self):
        response = self.client.get(reverse("shopapp:orders_export"))
        # self.assertTrue(self.user.is_staff, "User is not staff")
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user_id": order.user,
                "orders_list": [
                    product.pk for product in order.products
                ]
            }
            for order in orders
        ]
        order_data = response.json()
        self.assertEqual(
            order_data["orders"],
            expected_data
        )