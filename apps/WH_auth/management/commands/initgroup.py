from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.WH_goods.models import Goods
from apps.WH_scene.models import Scenes
from apps.WH_order.models import GoodsOrder
from apps.WH_index.models import Banner
from apps.WH_share.models import Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 管理员（管理景点、管理线路、管理订单、管理评论、管理轮播图
        edit_content_types = [
            ContentType.objects.get_for_model(Goods),
            ContentType.objects.get_for_model(Scenes),
            ContentType.objects.get_for_model(GoodsOrder),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        editGroup = Group.objects.create(name="管理员")
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('创建成功！'))


