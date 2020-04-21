from django.db import models


class Banner(models.Model):
    priority = models.IntegerField(default=0)
    image_url = models.URLField(null=True)
    link_to = models.URLField(null=True)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']
