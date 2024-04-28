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

# Định nghĩa view cho trang chính
def index(request):
    """
    Xử lý request và render trang chính của ứng dụng.

    Trang chính hiển thị các bài viết đặc biệt và các danh mục được đặt làm trang chủ.
    Các bài viết đặc biệt được lấy từ bảng Article với điều kiện special=True và status=APP_VALUE_STATUS_ACTIVE_DEFINE,
    sắp xếp theo ngày xuất bản giảm dần và giới hạn số lượng bài viết là 5.
    Các danh mục được lấy từ bảng Category với điều kiện status=APP_VALUE_STATUS_ACTIVE_DEFINE và is_homepage=True,
    sắp xếp theo thứ tự ordering.
    Mỗi danh mục còn có thêm thuộc tính article_filter là danh sách các bài viết thuộc danh mục đó, không phải bài viết đặc biệt,
    được sắp xếp theo ngày xuất bản giảm dần và giới hạn số lượng bài viết theo APP_VALUE_ARTICAL_NUM_MAX_HOMEPAGE_DEFINE.

    :param request: Đối tượng HttpRequest
    :return: Đối tượng HttpResponse chứa trang chính được render với các thông tin cần thiết
    """
    # Lấy các bài viết đặc biệt
    items_article_special = Article.objects.filter(special=True, status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now()).order_by("-publish_date")[:5]
    
    # Lấy các danh mục được đặt làm trang chủ
    items_category = Category.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE, is_homepage=True).order_by("ordering")

    # Lặp qua từng danh mục để tạo danh sách bài viết không phải đặc biệt thuộc danh mục đó
    for category in items_category:
        category.article_filter = category.article_set.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE, special=False, publish_date__lte=timezone.now()).order_by("-publish_date")[:APP_VALUE_ARTICAL_NUM_MAX_HOMEPAGE_DEFINE]

    # Lấy thông tin user agent của request
    user_agent = get_user_agent(request)

    # Render trang chính với các thông tin đã lấy được
    return render(request, TABLE_PATH_FILE + 'index.html', {
        "title_page": "Xuân Thu-Trang chủ",
        "items_article_special": items_article_special,
        "items_category": items_category,
    })

def category(request, category_slug):
    """
    Xử lý request để hiển thị danh sách bài viết thuộc một category cụ thể.

    :param request: HttpRequest object
    :param category_slug: Chuỗi slug của category
    :return: HttpResponse object chứa trang category được render với các thông tin cần thiết
    """
    # Lấy thông tin của category từ slug
    item_category = get_object_or_404(Category, slug=category_slug, status=APP_VALUE_STATUS_ACTIVE_DEFINE)
    
    # Lấy danh sách các bài viết thuộc category đó
    items_article = Article.objects.filter(category=item_category, status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now()).order_by("-publish_date")[:100]

    # Phân trang cho danh sách bài viết
    paginator = Paginator(items_article, APP_VALUE_ARTICAL_NUM_IN_PAGE_DEFINE)
    page = request.GET.get('page')
    items_article = paginator.get_page(page)

    return render(request, TABLE_PATH_FILE + 'category.html', {
        "title_page": item_category.name,
        "item_category": item_category,
        'items_article': items_article,
        'paginator': paginator,
    })

def article(request, article_slug, article_id):
    """
    Xử lý request để hiển thị chi tiết một bài viết cụ thể và các bài viết liên quan.

    :param request: HttpRequest object
    :param article_slug: Chuỗi slug của bài viết
    :param article_id: ID của bài viết
    :return: HttpResponse object chứa trang chi tiết bài viết được render với các thông tin cần thiết
    """
    # Lấy thông tin của bài viết từ slug và ID
    item_article = get_object_or_404(Article, id=article_id, slug=article_slug, status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now())
    
    # Lấy danh sách các bài viết liên quan thuộc cùng category
    items_article_related = Article.objects.filter(category=item_article.category, status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now()).order_by("-publish_date").exclude(slug=article_slug)[:APP_VALUE_ARTICAL_RELATED_MAX_DEFINE]

    return render(request, TABLE_PATH_FILE + 'article.html', {
        "item_article": item_article,
        "items_article_related": items_article_related,
        "title_page": item_article.name,
    })


def feed(request, feed_slug):
    """
    Xử lý request để lấy dữ liệu từ một feed cụ thể và hiển thị nó trên trang web.

    :param request: HttpRequest object
    :param feed_slug: Chuỗi slug của feed
    :return: HttpResponse object chứa trang web được render với dữ liệu từ feed và các thông tin cần thiết
    """
    # Lấy thông tin của feed từ slug
    item_feed = get_object_or_404(Feed, slug=feed_slug, status=APP_VALUE_STATUS_ACTIVE_DEFINE)

    # Xác nhận với SSL context nếu có
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    
    try:
        # Parse feed để lấy dữ liệu
        feed = feedparser.parse(item_feed.link)

        items_feed = []
        for entry in feed.entries:
            soup = BeautifulSoup(entry.summary, 'html.parser')
            img_tag = soup.find('img')
            img_src = APP_VALUE_DEFAULT_IMG_DEFINE
            if img_tag:
                img_src = img_tag['src']
            item = {
                'title': entry.title,
                'link': entry.link,
                'publish_date': entry.published,
                'img': img_src,
            }
            items_feed.append(item)
    except:
        # Xử lý ngoại lệ nếu có lỗi trong quá trình lấy dữ liệu từ feed
        print(f'Get article error {item_feed.link}')
        
    # Comment dưới đây chỉ để xem dữ liệu sau khi lấy về
    # with open ('feed.json','w', encoding='utf-8') as f:
    #     json.dump(feed,f, ensure_ascii=False)

    return render(request, TABLE_PATH_FILE + 'feed.html', {
        "title_page": "Tin tổng hợp - " + item_feed.name,
        "items_feed": items_feed,
        "item_feed": item_feed,
    })


def search(request):
    """
    Xử lý request để tìm kiếm bài viết dựa trên từ khóa và hiển thị kết quả.

    :param request: HttpRequest object
    :return: HttpResponse object chứa trang kết quả tìm kiếm được render với các thông tin cần thiết
    """
    # Lấy từ khóa tìm kiếm từ request GET
    keyword = request.GET.get("keyword")
    print(f'keyword={keyword}')
    
    # Tìm các bài viết chứa từ khóa trong tên và có trạng thái active
    items_article = Article.objects.filter(name__icontains=keyword, status=APP_VALUE_STATUS_ACTIVE_DEFINE)

    # Phân trang cho kết quả tìm kiếm
    paginator = Paginator(items_article, APP_VALUE_ARTICAL_NUM_IN_SEARCH_PAGE_DEFINE)
    page = request.GET.get('page')
    items_article = paginator.get_page(page)

    return render(request, TABLE_PATH_FILE + 'search.html', {
        "title_page": "Tìm kiếm cho từ khoá " + keyword,
        "items_article": items_article,
        "keyword": keyword,
        "paginator": paginator,
    })


def contact(request):
    """
    Xử lý request để hiển thị trang liên hệ.

    :param request: HttpRequest object
    :return: HttpResponse object chứa trang liên hệ được render với các thông tin cần thiết
    """
    return render(request, TABLE_PATH_FILE + 'contact.html', {
        "title_page": "Liên hệ"
    })


def about(request):
    """
    Xử lý request để hiển thị trang giới thiệu.

    :param request: HttpRequest object
    :return: HttpResponse object chứa trang giới thiệu được render với các thông tin cần thiết
    """
    return render(request, TABLE_PATH_FILE + 'about.html', {
        "title_page": "Giới thiệu"
    })


def policy(request):
    """
    Xử lý request để hiển thị trang điều khoản sử dụng.

    :param request: HttpRequest object
    :return: HttpResponse object chứa trang điều khoản sử dụng được render với các thông tin cần thiết
    """
    return render(request, TABLE_PATH_FILE + 'policy.html', {
        "title_page": "Điều khoản sử dụng"
    })
