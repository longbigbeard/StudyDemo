from django.db import models


class Goods(models.Model):
    title = models.CharField(max_length=200, null=True)
    sales = models.CharField(max_length=200, null=True)
    prices = models.CharField(max_length=200, null=True)
    goods_info = models.TextField(null=True)
    feature_info = models.TextField(null=True)
    schedule_goods = models.TextField(null=True)
    attention_goods = models.TextField(null=True)
    thumbnail = models.URLField(null=True)
    goods_video = models.URLField(null=True)

    pub_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey('WH_auth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['sales']
