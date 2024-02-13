from django.db import models
from django.urls import reverse

from tinymce.models import HTMLField
from news.helpers import *
from news.custom_field import *
from news.define import *

from .category import Category

# Create your models here.

class Article(models.Model):

    name = models.CharField(unique=True, max_length=500)
    slug = models.SlugField(unique=True, max_length=500)
    status = models.CharField(max_length=10,choices=APP_VALUE_STATUS_CHOICE, default=APP_VALUE_STATUS_DEFINE)
    ordering = models.IntegerField(default=0)
    special = CustomBooleanField()
    publish_date = models.DateTimeField()
    content = HTMLField()
    image = models.ImageField(upload_to=get_file_path,max_length=500,null=True,blank=True,verbose_name=(u'Contact list'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = TABLE_ARTICAL_SHOW #Đặt lại tên hiển thị
        constraints = [
        models.UniqueConstraint(fields=['name', 'slug'], name='unique_name_slug_constraint')
        ]

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("article", kwargs={"article_slug": self.slug, 'article_id':self.id})
    