from django.db import models
from django.urls import reverse

from news.helpers import *
from news.custom_field import *
from news.define import *

# Create your models here.
class Feed(models.Model):

    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    status = models.CharField(max_length=10,choices=APP_VALUE_STATUS_CHOICE, default=APP_VALUE_STATUS_DEFINE)
    ordering = models.IntegerField(default=0)
    link = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = TABLE_FEED_SHOW #Đặt lại tên hiển thị

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("feed", kwargs={"feed_slug": self.slug})