from django.contrib import admin

# Register your models here.
from .models import Category, Article, Feed


from .define import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','is_homepage', 'layout','ordering')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ['status','is_homepage', 'layout',] # tao chuc nang fillter
    search_fields = ['name'] # tao chuc nang search
    class Media:
        js = ADMIN_SRC_JS
        css = ADMIN_SRC_CSS

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name','category','status','ordering','special')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ['category','status','special'] # tao chuc nang fillter
    search_fields = ['name'] # tao chuc nang search
    class Media:
        js = ADMIN_SRC_JS
        css = ADMIN_SRC_CSS
   
class FeedAdmin(admin.ModelAdmin):
    list_display = ('name','status','ordering')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ['status'] # tao chuc nang fillter
    search_fields = ['name'] # tao chuc nang search
    class Media:
        js = ADMIN_SRC_JS
        css = ADMIN_SRC_CSS
   

admin.site.register(Category,CategoryAdmin) #Thêm vào site admin
admin.site.register(Article,ArticleAdmin)  #Thêm vào site admin
admin.site.register(Feed,FeedAdmin) #Thêm vào site admin

admin.site.site_header = ADMIN_SITE_NAME #Đặt lại tên cho site admin


