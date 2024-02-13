from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *
from .define import *

class StaticSitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['index','about','policy']

    def location(self, item):
        return reverse(item)

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'
    articles = Article.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE).order_by('-id')
    def items(self):
        return self.articles

    def location(self, obj):
        return f"/{obj.slug}-a{obj.id}.html"
        

    def lastmod(self, obj): 
        return obj.publish_date
    

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.filter(status=APP_VALUE_STATUS_DEFINE)

    def location(self, obj):
        return obj.get_absolute_url

    def lastmod(self, obj): 
        return obj.updated_at 