from rest_framework import serializers
from .models import Comment
from WH_auth.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'content', 'pub_time', 'author')

