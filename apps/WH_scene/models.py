from django.db import models


class Scenes(models.Model):
    title = models.CharField(max_length=200, null=True)
    ranking = models.CharField(max_length=100, null=True)
    grade = models.CharField(max_length=100, null=True)
    prices = models.CharField(max_length=100, null=True)
    scene_info = models.TextField(null=True)
    scene_desc = models.CharField(max_length=500, null=True)
    danger_info = models.TextField(null=True)
    thumbnail = models.URLField(null=True)
    bigimage = models.URLField(null=True)
    moreimage = models.TextField(null=True)
    scene_video = models.URLField(null=True)

    pub_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey('WH_auth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['ranking']

