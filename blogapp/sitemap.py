from django.contrib.sitemaps import Sitemap

from .models import ArticleR

class BlogSitemap(Sitemap):
    changefreg = "never"
    priority = 0.5

    def items(self):
        return (
           ArticleR.objects
           .filter(published_at__isnull=False)
           .order_by("-published_at")[:5]
        )

    def lastmod(selfs, obj: ArticleR):
        return obj.published_at