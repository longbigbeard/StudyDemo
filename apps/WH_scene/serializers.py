from rest_framework import serializers
from .models import Scenes


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenes
        fields = ('id', 'title', 'ranking', 'grade', 'scene_info', 'thumbnail',)
