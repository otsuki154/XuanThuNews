from django.contrib import admin
from .models import Category, Article, Feed
from .define import *

# Đăng ký các model vào trang admin

class CategoryAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện quản trị cho model Category.

    Thiết lập các trường hiển thị, trường tiền tố tự động cho trường slug, bộ lọc và tìm kiếm.
    """
    list_display = ('name', 'status', 'is_homepage', 'layout', 'ordering')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['status', 'is_homepage', 'layout']  # Tạo chức năng filter
    search_fields = ['name']  # Tạo chức năng search

    class Media:
        js = ADMIN_SRC_JS
        css = ADMIN_SRC_CSS

class ArticleAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện quản trị cho model Article.

    Thiết lập các trường hiển thị, trường tiền tố tự động cho trường slug, bộ lọc và tìm kiếm.
    """
    list_display = ('name', 'category', 'status', 'ordering', 'special')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'status', 'special']  # Tạo chức năng filter
    search_fields = ['name']  # Tạo chức năng search

    class Media:
        js = ADMIN_SRC_JS
        css = ADMIN_SRC_CSS

class FeedAdmin(admin.ModelAdmin):
    """
    Tùy chỉnh giao diện quản trị cho model Feed.

    Thiết lập các trường hiển thị, trường tiền tố tự động cho trường slug, bộ lọc và tìm kiếm.
    """
    list_display = ('name', 'status', 'ordering')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['status']  # Tạo chức năng filter
    search_fields = ['name']  # Tạo chức năng search

    class Media:
        js = ADMIN_SRC_JS
        css = ADMIN_SRC_CSS

# Thêm các model vào trang admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Feed, FeedAdmin)

# Đặt tên cho trang admin
admin.site.site_header = ADMIN_SITE_NAME
