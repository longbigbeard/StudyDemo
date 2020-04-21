from django.urls import path
from . import views

app_name = "WH_goods"

urlpatterns = [
    path('', views.index, name="index"),
    path('list/', views.goods_list, name="scenes_list"),
    path('<goods_id>/', views.goods_detail, name="goods_detail"),
]
