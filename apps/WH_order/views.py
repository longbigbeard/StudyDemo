from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from apps.utils import restful
from .forms import NewOrderForms
from apps.WH_goods.models import Goods
from apps.WH_order.models import GoodsOrder
from apps.WH_auth.decorators import wh_login_request


def index(request):
    return render(request, 'index/index.html')


@wh_login_request
@require_POST
def new_order(request):
    form = NewOrderForms(request.POST)
    if form.is_valid():
        which_time = form.cleaned_data.get("which_time")
        which_date = form.cleaned_data.get("which_date")
        person_nums = form.cleaned_data.get("person_nums")
        order_tel = form.cleaned_data.get("order_tel")
        order_info = form.cleaned_data.get("order_info")
        goods_pk = form.cleaned_data.get("goods_pk")

        if which_time == "time-am":
            which_time = "上午场"
        else:
            which_time = "下午场"

        if order_tel == '0':
            order_tel = request.user.telephone

        goods = Goods.objects.get(pk=int(goods_pk))
        prices = goods.prices.strip("￥")
        amount = int(prices) * int(person_nums)

        goods_order = GoodsOrder.objects.create(goods=goods, buyer=request.user, which_time=which_time,
                                                which_date=which_date, person_nums=person_nums, amount=amount,
                                                order_info=order_info, order_tel=order_tel, isdeal=1)

        return restful.result(data={"order_id": goods_order.pk})
    else:
        print("fail")
        return restful.params_error(message=form.errors)


@wh_login_request
def paying_order(request, order_id):
    order = GoodsOrder.objects.get(pk=order_id)
    order.goods.title = order.goods.title[:30] + "..."
    order.goods.prices = order.goods.prices.strip("￥")
    context = {
        "order": order,
    }
    return render(request, 'order/order-info.html', context=context)


@wh_login_request
def pay_order(request):
    istype = request.POST.get("istype")
    order_pk = request.POST.get("order_pk")

    GoodsOrder.objects.filter(pk=order_pk).update(istype=int(istype), status=2)
    return restful.ok()
