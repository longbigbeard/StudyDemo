from django.shortcuts import render
from .models import Goods
from django.conf import settings
import re
from apps.utils import restful
from .serializers import GoodsSerializer
from django.http import Http404
from apps.WH_auth.decorators import wh_login_request


def index(request):
    count = settings.ONE_PAGE_SCENE_GOODS_COUNT
    goods = Goods.objects.all()[0:count].values()

    for good in goods:
        good['feature_info'] = re.sub(r'<.*?>', '', good['feature_info'])
        good['feature_info'] = good['feature_info'].replace('\n', '')[:30] + "..."

    context = {
        "goods": goods,
    }
    return render(request, 'goods-info/goods-info-index.html', context=context)


def goods_list(request):
    # 通过p参数来获取第几页的数据
    # 并且P参数通过查询字符串的方式传过来的/scene/list/?p=2
    page = int(request.GET.get('p', 1))
    start = (page - 1) * settings.ONE_PAGE_SCENE_GOODS_COUNT
    ends = start + settings.ONE_PAGE_SCENE_GOODS_COUNT
    goods = Goods.objects.all()[start:ends].values()
    for good in goods:
        good['feature_info'] = re.sub(r'<.*?>', '', good['feature_info'])
        good['feature_info'] = good['feature_info'].replace('\n', '')[:30] + "..."

    serializer = GoodsSerializer(goods, many=True)
    data = serializer.data

    return restful.result(data=data)


@wh_login_request
def goods_detail(request, goods_id):
    try:
        goods = Goods.objects.get(pk=goods_id)
    except:
        raise Http404
    context = {
        'goods': goods
    }
    return render(request, 'goods-info/goods-info-detail.html', context=context)
