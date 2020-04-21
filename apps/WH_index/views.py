from django.shortcuts import render
from apps.WH_scene.models import Scenes
from apps.WH_goods.models import Goods
from apps.WH_share.models import Comment
from apps.WH_index.models import Banner
from django.conf import settings
import re


def index(request):
    count = settings.ONE_PAGE_SCENE_GOODS_SHARE_COUNT
    scenes = Scenes.objects.all()[0:count].values()
    for scene in scenes:
        scene['scene_info'] = re.sub(r'<.*?>', '', scene['scene_info'])
        scene['scene_info'] = scene['scene_info'].replace('\n', '')[:30] + "..."

    goods = Goods.objects.all()[0:count].values()
    for good in goods:
        good['feature_info'] = re.sub(r'<.*?>', '', good['feature_info'])
        good['feature_info'] = good['feature_info'].replace('\n', '')[:30] + "..."

    comments = Comment.objects.select_related('author').all()[0:count]
    banners = Banner.objects.all()[0:count]

    context = {
        "scenes": scenes,
        "goods": goods,
        "comments": comments,
        "banners": banners,
    }
    return render(request, 'index/index.html', context=context)


def attention(request):
    return render(request,'danger.html')