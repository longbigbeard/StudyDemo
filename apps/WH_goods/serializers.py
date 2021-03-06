from rest_framework import serializers
from .models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'title', 'sales', 'prices', 'feature_info', 'thumbnail',)
