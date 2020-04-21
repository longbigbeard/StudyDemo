from django.db import models


class Comment(models.Model):
    content = models.TextField(null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("WH_auth.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']
