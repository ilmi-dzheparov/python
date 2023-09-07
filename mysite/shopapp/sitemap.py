from django.contrib.sitemaps import Sitemap

from shopapp.models import Product


class ShopSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7
    def items(self):
        return Product.objects.order_by("pk").all()

    def lastmod(self, obj: Product):
        return obj.created_at

