from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Category, Article, Feed
from .define import *
from bs4 import BeautifulSoup
import feedparser
import ssl
import json
from django_user_agents.utils import get_user_agent
# Create your views here.

def index(request):

    items_article_special = Article.objects.filter(special=True, status=APP_VALUE_STATUS_ACTIVE_DEFINE , publish_date__lte = timezone.now()).order_by("-publish_date")[:5]
    items_category = Category.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE , is_homepage = True).order_by("ordering")

    for category in items_category:
        category.article_filter = category.article_set.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE, special=False , publish_date__lte = timezone.now()).order_by("-publish_date")[:APP_VALUE_ARTICAL_NUM_MAX_HOMEPAGE_DEFINE]
    user_agent = get_user_agent(request)

    return render(request, TABLE_PATH_FILE + 'index.html',{
        "title_page":"Xuân Thu-Trang chủ",
        "items_article_special":items_article_special,
        "items_category":items_category,
    })

def category(request,category_slug):
    # category_slug => thông tin category => article thuộc catagoru -> đổ dữ liệu ra phía client
    #lấy thông tin catarory
    item_category = get_object_or_404(Category, slug=category_slug, status=APP_VALUE_STATUS_ACTIVE_DEFINE )
    #lấy article thuộc catarory
    items_article = Article.objects.filter(category=item_category, status=APP_VALUE_STATUS_ACTIVE_DEFINE , publish_date__lte = timezone.now()).order_by("-publish_date")

    #phân trang
    paginator = Paginator(items_article, APP_VALUE_ARTICAL_NUM_IN_PAGE_DEFINE)
    page = request.GET.get('page')

    items_article = paginator.get_page(page)

    return render(request, TABLE_PATH_FILE + 'category.html',{
        "title_page"    :item_category.name,
        "item_category" :item_category,
        'items_article' :items_article,
        'paginator'     :paginator,
    })


def article(request,article_slug,article_id):

      #lấy thông tin catarory
    item_article = get_object_or_404(Article, id=article_id, slug=article_slug,status=APP_VALUE_STATUS_ACTIVE_DEFINE , publish_date__lte = timezone.now())
    items_article_related = Article.objects.filter(category=item_article.category, status=APP_VALUE_STATUS_ACTIVE_DEFINE , publish_date__lte = timezone.now()).order_by("-publish_date").exclude(slug=article_slug)[:APP_VALUE_ARTICAL_RELATED_MAX_DEFINE]

    return render(request, TABLE_PATH_FILE + 'article.html',{
        "item_article"          :item_article,
        "items_article_related" :items_article_related,
        "title_page"            :item_article.name,
    })

def feed(request,feed_slug):
    item_feed = get_object_or_404(Feed, slug=feed_slug,status=APP_VALUE_STATUS_ACTIVE_DEFINE )
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    try:
        feed = feedparser.parse(item_feed.link)

        items_feed = []
        for entry in feed.entries:
            soup = BeautifulSoup(entry.summary,'html.parser')
            img_tag = soup.find('img')
            img_src = APP_VALUE_DEFAULT_IMG_DEFINE
            if img_tag:
                img_src = img_tag['src']
            item = {
                'title'         :entry.title,
                'link'          :entry.link,
                'title'         :entry.title,
                'publish_date'  :entry.published,
                'img'           :img_src,
            }
            items_feed.append(item)
    except:
        print(f'Get article error {item_feed.link}')
        
    # chỉ để xem dữ liệu sau khi lấy về
    # with open ('feed.json','w', encoding='utf-8') as f:
    #     json.dump(feed,f, ensure_ascii=False)

    return render(request, TABLE_PATH_FILE + 'feed.html',{
        "title_page"    :"Tin tổng hợp - "+item_feed.name,
        "items_feed"    :items_feed,
        "item_feed"     :item_feed,
    })

def search(request):
    keyword = request.GET.get("keyword")
    print(f'keyword={keyword}')
    items_article = Article.objects.filter(name__icontains=keyword, status=APP_VALUE_STATUS_ACTIVE_DEFINE )

    #phân trang
    paginator = Paginator(items_article, APP_VALUE_ARTICAL_NUM_IN_SEARCH_PAGE_DEFINE)
    page = request.GET.get('page')
    
    items_article = paginator.get_page(page)

    return render(request, TABLE_PATH_FILE + 'search.html',{
        "title_page"    :"Tìm kiếm cho từ khoá " + keyword,
        "items_article" :items_article,
        "keyword"       :keyword,
        "paginator"     :paginator,
    })

def contact(request):


    return render(request, TABLE_PATH_FILE + 'contact.html',{
        "title_page":"Liên hệ"

    })

def about(request):


    return render(request, TABLE_PATH_FILE + 'about.html',{
        "title_page":"Giới thiệu"

    })

def policy(request):


    return render(request, TABLE_PATH_FILE + 'policy.html',{
        "title_page":"Điều khoản sử dụng"

    })
