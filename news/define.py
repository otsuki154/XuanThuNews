APP_VALUE_LAYOUT_DEFINE = "list"
APP_VALUE_STATUS_DEFINE = "draft"
APP_VALUE_STATUS_ACTIVE_DEFINE = "published"

APP_VALUE_ARTICAL_NUM_IN_PAGE_DEFINE = 10
APP_VALUE_ARTICAL_NUM_IN_SEARCH_PAGE_DEFINE = 10
APP_VALUE_ARTICAL_RELATED_MAX_DEFINE = 4
APP_VALUE_ARTICAL_NUM_MAX_HOMEPAGE_DEFINE = 4

APP_VALUE_CATAGORY_NUM_MENU_SIDEBAR_DEFINE = 8

APP_VALUE_FEED_NUM_MENU_SIDEBAR_DEFINE = 5
APP_VALUE_FEED_NUM_RECENT_SIDEBAR_DEFINE = 5
APP_VALUE_FEED_NUM_RANDOM_FOOTER_DEFINE = 3
APP_VALUE_FEED_NUM_TRENDING_FOOTER_DEFINE = 1

APP_VALUE_COIN_NUM_SIDEBAR_DEFINE = 8
APP_VALUE_COIN_EXCLUDE_SIDEBAR_DEFINE = ["Tether USDt", "USDC"]
APP_VALUE_COIN_URL_SIDEBAR_DEFINE = "http://apiforlearning.zendvn.com/api/get-coin"

APP_VALUE_GOLD_URL_SIDEBAR_DEFINE = "http://apiforlearning.zendvn.com/api/get-gold"
APP_VALUE_COIN_NUM_SIDEBAR_DEFINE = 8

APP_VALUE_GOLD_NUM_SIDEBAR_DEFINE = 5
APP_VALUE_DEFAULT_IMG_DEFINE = '/media/news/images/feed/logo.png'
APP_VALUE_LOGO_IMG_DEFINE = '/media/news/images/feed/logo.png'
APP_VALUE_SMALL_LOGO_IMG_DEFINE = '/media/news/images/feed/logo_small.png'
APP_VALUE_FOOTER_IMG_DEFINE = '/media/news/images/feed/world-news.png'
APP_VALUE_404_IMG_DEFINE = '/media/news/images/feed/404.png'
TABLE_CATEGORY_SHOW = "Category"
TABLE_ARTICAL_SHOW = "Articles"
TABLE_FEED_SHOW = "Feeds"
TABLE_PATH_FILE = "pages/"


ADMIN_SRC_JS = ('admin/js/slugify.min.js','admin/js/jquery-3.6.0.min.js','admin/js/general.js') #tao auto slug bang tieng Viet
ADMIN_SRC_CSS = {'all':('admin/css/custome.css',)} #tao custome css cho các BooleanFiled
ADMIN_SITE_NAME = "Xuân Thu Admin site"

APP_VALUE_LAYOUT_CHOICE = (
    ('list','List'),
    ('grid', 'Grid')
)
APP_VALUE_STATUS_CHOICE = (
    ('draft','Draft'),
    ('published', 'Published')
)