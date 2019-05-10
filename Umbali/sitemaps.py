from django.urls import reverse
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):

    def items(self):
        return ['Web:index','Web:contact']

    def location(self, item):
        return reverse(item)
