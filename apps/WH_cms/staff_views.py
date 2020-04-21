from django.shortcuts import render, reverse, redirect
from apps.WH_auth.models import User
from django.views import View
from django.contrib.auth.models import Group
from apps.WH_auth.decorators import wh_superuser_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from apps.utils import restful


@wh_superuser_required
def staffs_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        "staffs": staffs,
    }
    return render(request, 'cms/staffs.html', context=context)


@method_decorator(wh_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            "groups": groups,
        }
        return render(request, 'cms/add_staffs.html', context=context)

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            group_ids = request.POST.get('groups')
            group = Group.objects.filter(pk__in=group_ids)
            user.groups.set(group)
            user.save()
            return redirect(reverse('WH_cms:staffs'))
        else:
            messages.info(request, '手机号码不存在')
            return redirect(reverse('WH_cms:add_staffs'))


@wh_superuser_required
def del_staffs_view(request):
    staff_id = request.POST.get('staff_id')
    User.objects.filter(pk=staff_id).update(is_staff=False)
    return restful.ok()
