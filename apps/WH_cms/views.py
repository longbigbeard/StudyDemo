import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.utils import restful
from .forms import WriteScenesForms, WriteGoodsForm, AddBannerForm, EditBannerForm, EditScenesForms, EditGoodsForms
from apps.WH_scene.models import Scenes
from apps.WH_goods.models import Goods
from apps.WH_index.models import Banner
from apps.WH_share.models import Comment
from apps.WH_order.models import GoodsOrder
from apps.WH_index.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


@require_POST
def upload_img_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})


@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')


@method_decorator(permission_required(perm='WH_scene.add_scenes', login_url='/'), name='dispatch')
class WriteScenesView(View):

    def get(self, request):
        return render(request, 'cms/write_scene.html')

    def post(self, request):
        form = WriteScenesForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            ranking = form.cleaned_data.get('ranking')
            prices = form.cleaned_data.get('prices')
            grade = form.cleaned_data.get('grade')
            scene_info = form.cleaned_data.get('scene_info')
            danger_info = form.cleaned_data.get('danger_info')
            thumbnail = form.cleaned_data.get('thumbnail')
            bigimage = form.cleaned_data.get('bigimage')
            moreimage = form.cleaned_data.get('moreimage')
            scene_video = form.cleaned_data.get('scene_video')

            Scenes.objects.create(title=title, ranking=ranking, prices=prices, grade=grade,
                                  scene_info=scene_info, danger_info=danger_info,
                                  thumbnail=thumbnail, bigimage=bigimage, moreimage=moreimage,
                                  scene_video=scene_video, author=request.user)
            return restful.ok()
        else:
            print("fail")
            return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm='WH_scene.change_scenes', login_url='/'), name='dispatch')
class OperateScene(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')

        scene = Scenes.objects.select_related('author').all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            scene = scene.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            scene = scene.filter(title__icontains=title)

        paginator = Paginator(scene, 2)
        if page > paginator.num_pages:
            page = paginator.num_pages
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            "scenes": page_obj.object_list,
            "page_obj": page_obj,
            "paginator": paginator,
            'start': start,
            'end': end,
            'title': title,
            "url_query": '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
            }),
        }
        context.update(context_data)
        return render(request, 'cms/operate_scene.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            # 当前页面
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@method_decorator(permission_required(perm='WH_scene.change_scenes', login_url='/'), name='dispatch')
class EditScene(View):
    def get(self, request):
        scene_id = request.GET.get('scene_id')
        scene = Scenes.objects.get(pk=scene_id)

        context = {
            "scene": scene,
        }
        return render(request, 'cms/write_scene.html', context=context)

    def post(self, request):
        form = EditScenesForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            ranking = form.cleaned_data.get('ranking')
            prices = form.cleaned_data.get('prices')
            grade = form.cleaned_data.get('grade')
            scene_info = form.cleaned_data.get('scene_info')
            danger_info = form.cleaned_data.get('danger_info')
            thumbnail = form.cleaned_data.get('thumbnail')
            bigimage = form.cleaned_data.get('bigimage')
            moreimage = form.cleaned_data.get('moreimage')
            scene_video = form.cleaned_data.get('scene_video')
            pk = form.cleaned_data.get('pk')

            Scenes.objects.filter(pk=pk).update(title=title, ranking=ranking, prices=prices, grade=grade,
                                                scene_info=scene_info, danger_info=danger_info,
                                                thumbnail=thumbnail, bigimage=bigimage, moreimage=moreimage,
                                                scene_video=scene_video, author=request.user)
            return restful.ok()
        else:
            print("file")
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='WH_scene.delete_scenes', login_url='/')
def delete_scene(request):
    scene_id = request.POST.get("scene_id")
    Scenes.objects.filter(pk=scene_id).delete()
    return restful.ok()


@method_decorator(permission_required(perm='WH_goods.add_goods', login_url='/'), name='dispatch')
class WriteGoodsView(View):
    def get(self, request):
        return render(request, 'cms/write_goods.html')

    def post(self, request):
        form = WriteGoodsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            sales = form.cleaned_data.get('sales')
            prices = form.cleaned_data.get('prices')
            goods_info = form.cleaned_data.get('goods_info')
            feature_info = form.cleaned_data.get('feature_info')
            schedule_goods = form.cleaned_data.get('schedule_goods')
            attention_goods = form.cleaned_data.get('attention_goods')
            thumbnail = form.cleaned_data.get('thumbnail')
            goods_video = form.cleaned_data.get('goods_video')

            print(sales)

            Goods.objects.create(title=title, sales=sales, prices=prices, goods_info=goods_info,
                                 feature_info=feature_info,
                                 schedule_goods=schedule_goods, attention_goods=attention_goods, thumbnail=thumbnail,
                                 goods_video=goods_video, author=request.user)
            return restful.ok()

        else:
            print("fail")
            return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm='WH_goods.change_goods', login_url='/'), name='dispatch')
class OperateGoodsView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')

        goods = Goods.objects.select_related('author').all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            goods = goods.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            goods = goods.filter(title__icontains=title)

        paginator = Paginator(goods, 2)
        if page > paginator.num_pages:
            page = paginator.num_pages
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            "goods": page_obj.object_list,
            "page_obj": page_obj,
            "paginator": paginator,
            'start': start,
            'end': end,
            'title': title,
            "url_query": '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
            }),
        }
        context.update(context_data)
        return render(request, 'cms/operate_goods.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            # 当前页面
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@method_decorator(permission_required(perm='WH_goods.change_goods', login_url='/'), name='dispatch')
class EditGoods(View):
    def get(self, request):
        goods_id = request.GET.get('goods_id')
        goods = Goods.objects.get(pk=goods_id)

        context = {
            "goods": goods,
        }
        return render(request, 'cms/write_goods.html', context=context)

    def post(self, request):
        form = EditGoodsForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            sales = form.cleaned_data.get('sales')
            prices = form.cleaned_data.get('prices')
            goods_info = form.cleaned_data.get('goods_info')
            feature_info = form.cleaned_data.get('feature_info')
            schedule_goods = form.cleaned_data.get('schedule_goods')
            attention_goods = form.cleaned_data.get('attention_goods')
            thumbnail = form.cleaned_data.get('thumbnail')
            goods_video = form.cleaned_data.get('goods_video')
            pk = form.cleaned_data.get('pk')

            Goods.objects.filter(pk=pk).update(title=title, sales=sales, prices=prices, goods_info=goods_info,
                                               feature_info=feature_info,
                                               schedule_goods=schedule_goods, attention_goods=attention_goods,
                                               thumbnail=thumbnail,
                                               goods_video=goods_video, author=request.user)
            return restful.ok()
        else:
            print("fail")
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='WH_goods.delete_goods', login_url='/')
def delete_goods(request):
    goods_id = request.POST.get("goods_id")
    Goods.objects.filter(pk=goods_id).delete()
    return restful.ok()


@permission_required(perm='WH_index.add_banner', login_url='/')
def banners(request):
    return render(request, 'cms/banners.html')


@permission_required(perm='WH_index.add_banner', login_url='/')
def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)

        return restful.result(data={"banner_id": banner.pk})
    else:
        print("创建轮播图模型错误")
        return restful.params_error(message=form.get_errors())


@permission_required(perm='WH_index.change_banner', login_url='/')
def banner_list(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return restful.result(data=serializer.data)


@permission_required(perm='WH_index.delete_banner', login_url='/')
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


@permission_required(perm='WH_index.change_banner', login_url='/')
def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        image_url = form.cleaned_data.get('image_url')
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')

        Banner.objects.filter(pk=pk).update(priority=priority, image_url=image_url, link_to=link_to)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm='WH_share.change_comment', login_url='/'), name='dispatch')
class OperateShareView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')

        comments = Comment.objects.all()

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            comments = comments.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            comments = comments.filter(title__icontains=title)

        paginator = Paginator(comments, 2)
        if page > paginator.num_pages:
            page = paginator.num_pages
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            "comments": page_obj.object_list,
            "page_obj": page_obj,
            "paginator": paginator,
            'start': start,
            'end': end,
            'title': title,
            "url_query": '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
            }),
        }
        context.update(context_data)
        return render(request, 'cms/operate_share.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            # 当前页面
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@require_POST
@permission_required(perm='WH_share.delete_comment', login_url='/')
def delete_share(request):
    comment_id = request.POST.get("comment_id")
    Comment.objects.filter(pk=comment_id).delete()
    return restful.ok()


@method_decorator(permission_required(perm='WH_order.change_goodsorder', login_url='/'), name='dispatch')
class OperateOrderView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        order_tel = request.GET.get('order_tel')
        isdeal = request.GET.get('isdeal')
        isrem = request.GET.get('isrem')
        isnew = request.GET.get('isnew')

        orders = GoodsOrder.objects.select_related('goods', 'buyer').all()
        # 根据时间查询
        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            orders = orders.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))
        # 根据用户输入查询
        if order_tel:
            orders = orders.filter(order_tel__icontains=order_tel)
        # 根据是否处理查询
        if isdeal == "0":
            orders = orders.filter(isdeal=0)
        elif isdeal == "1":
            orders = orders.filter(isdeal=1)
        # 根据退订查询
        if isrem == "3":
            orders = orders.filter(status=3)
        elif isrem == "4":
            orders = orders.filter(status=4)
        # 根据是否是新订单查询
        if isnew == "1":
            orders = orders.filter(isdeal=1)
            orders = orders.filter(status=2)
        # 转义为文本
        for order in orders:
            if order.istype == 1:
                order.istype = "支付宝"
            elif order.istype == 2:
                order.istype = "微信"
            else:
                order.istype = "无"

            if order.status == 1:
                order.status = "未支付"
            elif order.status == 2:
                order.status = "已付款"
            elif order.status == 4:
                order.status = "退款中"
            else:
                order.status = "已退款"

            if order.isdeal == 0:
                order.isdeal = "是"
            else:
                order.isdeal = "否"

            if not order.order_info:
                order.order_info = "无"

            order.goods.title = order.goods.title[:10] + "..."
        paginator = Paginator(orders, 2)
        if page > paginator.num_pages:
            page = paginator.num_pages
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            "orders": page_obj.object_list,
            "page_obj": page_obj,
            "paginator": paginator,
            'start': start,
            'end': end,
            'order_tel': order_tel,
            'isdeal': isdeal,
            'isrem': isrem,
            'isnew': isnew,
            "url_query": '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'order_tel': order_tel or '',
                'isdeal': isdeal,
                'isrem': isrem,
                'isnew': isnew,
            }),
        }
        context.update(context_data)
        return render(request, 'cms/operate_order.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            # 当前页面
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@require_POST
@permission_required(perm='WH_order.change_goodsorder', login_url='/')
def deal_order(request):
    order_id = request.POST.get("order_id")
    order = GoodsOrder.objects.get(pk=order_id)
    status = 3
    if order.status == 4:
        GoodsOrder.objects.filter(pk=order_id).update(isdeal=0, status=status)
    GoodsOrder.objects.filter(pk=order_id).update(isdeal=0)
    return restful.ok()
