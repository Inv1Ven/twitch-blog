from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from streamers.sitemaps import PostSitemap, StaticViewSitemap

# Регистрируем карты сайта
sitemaps = {
    'posts': PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('streamers.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Раздаем медиа-файлы (картинки) ВСЕГДА, даже когда DEBUG=False
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
