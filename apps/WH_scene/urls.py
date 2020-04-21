from django.urls import path
from . import views

app_name = "WH_scene"

urlpatterns = [
    path('', views.index, name="index"),
    path('list/', views.scenes_list, name="scenes_list"),
    path('<scenes_id>/', views.scene_detail, name="scenes_detail"),
]
