from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemap import ArticleSitemap, StaticSitemap,CategorySitemap
from django.views.generic import TemplateView

sitemaps = {
    'category':CategorySitemap,
    # 'article':ArticleSitemap,
    # 'static': StaticSitemap,
}

urlpatterns = [

    path('', views.index, name = "index"),
    
    # path('category/<slug:category_slug>', views.category, name = "category"),
    # path('article/<slug:article_slug>', views.article, name = "article"),
    # path('<slug:feed_slug>', views.feed, name = "feed"),
    path('search.html', views.search, name = "search"),
    path('contact.html', views.contact, name = "contact"),
    path('about.html', views.about, name = "about"),
    path('policy.html', views.policy, name = "policy"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),

    path('sitemap.xml', sitemap, {'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),

    re_path(r'^tin-tong-hop-(?P<feed_slug>[\w-]+)\.html$', views.feed, name='feed'),
    re_path(r'^(?P<article_slug>[\w-]+)-a(?P<article_id>\d+)\.html$', views.article, name='article'),

    path('<slug:category_slug>.html', views.category, name = "category"),
    path('tinymce/', include('tinymce.urls')),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
