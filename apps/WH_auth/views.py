from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm, EditPasswordForm
from django.http import JsonResponse
from utils import restful
from utils.captcha.myaptcha import Captcha
from io import BytesIO
from django.core.cache import cache
from django.contrib.auth import get_user_model
from apps.WH_order.models import GoodsOrder
from apps.WH_share.models import Comment
from apps.WH_auth.decorators import wh_login_request

User = get_user_model()


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="您的账号被冻结了！")
        else:
            return restful.params_error(message="您的手机号码或者是密码错误！")
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('WH_index:index'))


@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())


def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO 相当于一个管道，用来存储图片的数据流
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 将图形验证码存储到缓存中,变成小写
    cache.set(text.lower(), text.lower(), 5 * 60)

    return response


@wh_login_request
def edit_password(request):
    return render(request, 'person-info/edit_password.html')


@require_POST
@wh_login_request
def edit_author_info(request):
    forms = EditPasswordForm(request.POST)
    if forms.is_valid():
        author_name = forms.cleaned_data.get("author_name")
        author_passwd = forms.cleaned_data.get("author_passwd")
        author_id = request.user.pk
        User.objects.filter(pk=author_id).update(username=author_name, password=author_passwd)
        return restful.ok()
    else:
        return restful.params_error(forms.errors)


@wh_login_request
def edit_order(request):
    user_id = request.user.pk
    order = GoodsOrder.objects.select_related('goods', 'buyer').all()
    orders = order.filter(buyer_id=user_id)

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

    context = {
        "orders": orders,
    }

    return render(request, 'person-info/edit_order.html', context=context)


@require_POST
@wh_login_request
def edit_order_info(request):
    order_id = request.POST.get("order_id")
    GoodsOrder.objects.filter(pk=order_id).update(status=4, isdeal=1)
    return restful.ok()


@wh_login_request
def edit_share(request):
    author_id = request.user.pk
    comments = Comment.objects.filter(author_id=author_id).all()
    context = {
        "comments": comments,
    }
    return render(request, 'person-info/edit_share.html', context=context)


@require_POST
@wh_login_request
def edit_share_info(request):
    comment_id = request.POST.get("comment_id")
    Comment.objects.filter(pk=comment_id).delete()
    return restful.ok()
