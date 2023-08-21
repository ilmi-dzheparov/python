from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailView,
    ProductsListView,
    OrdersListView,
    OrderDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ProductsDataExportView,
    OrdersDataExportView,
    # create_order,
)


app_name = "shopapp"
urlpatterns = [
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="products_export"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="products_detail"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrdersDataExportView.as_view(), name="orders_export"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]
