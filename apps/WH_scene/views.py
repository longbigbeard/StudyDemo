from django.shortcuts import render
from django.http import Http404
import re

from .models import Scenes
from django.conf import settings
from utils import restful
from .serializers import SceneSerializer


def index(request):
    count = settings.ONE_PAGE_SCENE_GOODS_COUNT
    scenes = Scenes.objects.all()[0:count].values()

    for scene in scenes:
        scene['scene_info'] = re.sub(r'<.*?>', '', scene['scene_info'])
        scene['scene_info'] = scene['scene_info'].replace('\n', '')[:30] + "..."

    context = {
        "scenes": scenes,
    }
    return render(request, 'scene-info/scene-info-index.html', context=context)


def scenes_list(request):
    # 通过p参数来获取第几页的数据
    # 并且P参数通过查询字符串的方式传过来的/scene/list/?p=2
    page = int(request.GET.get('p', 1))
    start = (page - 1) * settings.ONE_PAGE_SCENE_GOODS_COUNT
    ends = start + settings.ONE_PAGE_SCENE_GOODS_COUNT
    scenes = Scenes.objects.all()[start:ends].values()
    for scene in scenes:
        scene['scene_info'] = re.sub(r'<.*?>', '', scene['scene_info'])
        scene['scene_info'] = scene['scene_info'].replace('\n', '')[:30] + "..."
    serializer = SceneSerializer(scenes, many=True)
    data = serializer.data

    return restful.result(data=data)


def scene_detail(request, scenes_id):
    try:
        scene = Scenes.objects.get(pk=scenes_id)
    except:
        raise Http404
    context = {
        'scene': scene
    }
    return render(request, 'scene-info/scene-info-detail.html', context=context)
