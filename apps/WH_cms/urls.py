from django.urls import path
from . import views, staff_views

app_name = 'WH_cms'

urlpatterns = [
    path("", views.index, name='index'),
    path("write_scenes/", views.WriteScenesView.as_view(), name='write_scenes'),
    path("operate_scene/", views.OperateScene.as_view(), name='operate_scene'),
    path("edit_scene/", views.EditScene.as_view(), name='edit_scene'),
    path("delete_scene/", views.delete_scene, name='delete_scene'),
    path("write_goods/", views.WriteGoodsView.as_view(), name='write_goods'),
    path("operate_goods/", views.OperateGoodsView.as_view(), name='operate_goods'),
    path("edit_goods/", views.EditGoods.as_view(), name='edit_goods'),
    path("delete_goods/", views.delete_goods, name='delete_goods'),
    path("upload_img_file/", views.upload_img_file, name='upload_img_file'),
    path("banner/", views.banners, name='banner'),
    path("add_banner/", views.add_banner, name='add_banner'),
    path("banner_list/", views.banner_list, name='banner_list'),
    path("delete_banner/", views.delete_banner, name='delete_banner'),
    path("edit_banner/", views.edit_banner, name='edit_banner'),
    path("operate_share/", views.OperateShareView.as_view(), name='operate_share'),
    path("delete_share/", views.delete_share, name='delete_share'),
    path("operate_order/", views.OperateOrderView.as_view(), name='operate_order'),
    path("deal_order/", views.deal_order, name='deal_order'),
]

# 员工管理
urlpatterns += [
    path("staffs", staff_views.staffs_view, name='staffs'),
    path("add_staff/", staff_views.AddStaffView.as_view(), name='add_staffs'),
    path("delete_staff/", staff_views.del_staffs_view, name='del_staffs'),
]
