from .models import Category, Feed, Article
from django.utils import timezone
from .define import *
from .helpers import *
from django.db.models import Count
import requests
from datetime import datetime
from django_user_agents.utils import get_user_agent

def items_category_sidebar_menu(request):
    """
    Trả về danh sách các danh mục để hiển thị trong menu bên thanh sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin các danh mục và các hằng số hỗ trợ hiển thị giao diện
    """
    items_category_sidebar_menu = Category.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE).order_by("ordering").annotate(num_article=Count('article'))[:APP_VALUE_CATAGORY_NUM_MENU_SIDEBAR_DEFINE]
    return {
        "items_category_sidebar_menu": items_category_sidebar_menu,
        "logo_image": APP_VALUE_LOGO_IMG_DEFINE,
        "small_logo_image": APP_VALUE_SMALL_LOGO_IMG_DEFINE,
        "img_src": APP_VALUE_DEFAULT_IMG_DEFINE,
        "404_img_src": APP_VALUE_404_IMG_DEFINE,
    }

def items_feed_sidebar_menu(request):
    """
    Trả về danh sách các feed để hiển thị trong menu bên thanh sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin các feed và thời gian hiện tại
    """
    items_feed_sidebar_menu = Feed.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE).order_by("ordering")[:APP_VALUE_FEED_NUM_MENU_SIDEBAR_DEFINE]
    today = datetime.now().strftime("%A, %d/%m/%Y")  # Lấy thời gian hiện tại và chuyển định dạng
    return {
        "items_feed_sidebar_menu": items_feed_sidebar_menu,
        "today": today
    }

def items_feed_sidebar_recent(request):
    """
    Trả về danh sách các bài viết mới nhất để hiển thị trong sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin các bài viết mới nhất
    """
    skip_slug = get_skip_slug_article(request.path)
    items_feed_sidebar_recent = Article.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now()).order_by("-publish_date").exclude(slug=skip_slug)[:APP_VALUE_FEED_NUM_RECENT_SIDEBAR_DEFINE]
    return {"items_feed_sidebar_recent": items_feed_sidebar_recent}

def items_feed_sidebar_random(request):
    """
    Trả về danh sách các bài viết ngẫu nhiên để hiển thị trong sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin các bài viết ngẫu nhiên và các hằng số hỗ trợ hiển thị giao diện
    """
    skip_slug = get_skip_slug_article(request.path)
    items_feed_sidebar_random = Article.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now()).order_by("?").exclude(slug=skip_slug)[:APP_VALUE_FEED_NUM_RANDOM_FOOTER_DEFINE]
    return {
        "items_feed_sidebar_random": items_feed_sidebar_random,
        "img_src": APP_VALUE_DEFAULT_IMG_DEFINE,
        "footer_img_src": APP_VALUE_FOOTER_IMG_DEFINE,
    }

def items_feed_sidebar_trending(request):
    """
    Trả về danh sách các bài viết nổi bật để hiển thị trong sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin các bài viết nổi bật
    """
    skip_slug = get_skip_slug_article(request.path)
    items_feed_sidebar_trending = Article.objects.filter(status=APP_VALUE_STATUS_ACTIVE_DEFINE, publish_date__lte=timezone.now()).order_by("?").exclude(slug=skip_slug)[:APP_VALUE_FEED_NUM_TRENDING_FOOTER_DEFINE]
    return {"items_feed_sidebar_trending": items_feed_sidebar_trending}

def items_price_sidebar_coin(request):
    """
    Trả về thông tin giá coin để hiển thị trong sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin giá coin
    """
    items_price_sidebar_coin = []
    response = requests.get(APP_VALUE_COIN_URL_SIDEBAR_DEFINE)
    try:
        if response.status_code == 200:
            data = response.json()[:APP_VALUE_COIN_NUM_SIDEBAR_DEFINE]
            items_price_sidebar_coin = [item for item in data if item["name"] not in APP_VALUE_COIN_EXCLUDE_SIDEBAR_DEFINE]
    except:
        print(f'Get coin error from server API {APP_VALUE_COIN_URL_SIDEBAR_DEFINE}')
    return {"items_price_sidebar_coin": items_price_sidebar_coin}

def items_price_sidebar_gold(request):
    """
    Trả về thông tin giá vàng để hiển thị trong sidebar.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin giá vàng
    """
    items_price_sidebar_gold = []
    response = requests.get(APP_VALUE_GOLD_URL_SIDEBAR_DEFINE)
    try:
        if response.status_code == 200:
            items_price_sidebar_gold = response.json()[:APP_VALUE_GOLD_NUM_SIDEBAR_DEFINE]
    except:
        print(f'Get coin error from server API {APP_VALUE_COIN_URL_SIDEBAR_DEFINE}')
    return {"items_price_sidebar_gold": items_price_sidebar_gold}

def isMobileUser(request):
    """
    Xác định xem người dùng là thiết bị di động hay không.

    :param request: Đối tượng HttpRequest
    :return: Dictionary chứa thông tin xác định người dùng là thiết bị di động hay không
    """
    user_agent = get_user_agent(request)
    print(f'isMobileUser {user_agent.is_mobile}')
    return {"isMobileUser": user_agent.is_mobile}
