from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{id}/preview/{filename}".format(
        id=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """
    Модель Product представляет товар, который можно продавать в интернет магазине.

    Заказы тут: :model:`shopapp.Order`
    """

    class Meta:
        ordering = ["name", "price"]
        # db_table = "tech_products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    preview = models.FileField(
        null=True, blank=True, upload_to=product_preview_directory_path
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    archived = models.BooleanField(default=False)

    # @property
    # def description_short(self)->str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + '...'

    def get_absolute_url(self):
        return reverse("shopapp:products_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f'Product (pk={self.pk}, name="{self.name}")'


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to="orders/receipts/")

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{id}/images/{filename}".format(
        id=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)
