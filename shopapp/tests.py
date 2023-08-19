from random import choices
from string import ascii_letters

from django.contrib.auth.models import User, Permission
from django.shortcuts import reverse
from django.test import TestCase

from .models import Product
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


