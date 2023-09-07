from django import forms
from django.contrib.auth.models import User, Group
from django.core import validators
from django.forms import Textarea, ModelForm

from shopapp.models import Product, Order


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name",)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={"multiple": True})
    # )


class OrderForm(forms.ModelForm):
    # delivery_address = forms.CharField(null=True, blank=True)
    # promocode = forms.CharField(max_length=20, null=False, blank=True)
    # user = forms.Select(User)
    products = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Product.objects.all().order_by("pk"),
    )

    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user"


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(
#         label="Product description",
#         widget=forms.Textarea(attrs={"rows":5, "cols":30}),
#         validators=[validators.RegexValidator(
#             regex=r'great',
#             message="Field must contain word 'great'",
#         )]
#     )
