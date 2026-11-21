from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'  
    priority = 0.9         

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['streamers:post_list']

    def location(self, item):
        return reverse(item)