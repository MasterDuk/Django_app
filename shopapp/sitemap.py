from django.contrib.sitemaps import Sitemap

from .models import Product

class ShopSitemap(Sitemap):
    changefreg = "never"
    priority = 0.5

    def items(self):
        return (
           Product.objects
           .filter(created_at__isnull=False)
           .order_by("-created_at")
        )

    def lastmod(selfs, obj: Product):
        return obj.created_at