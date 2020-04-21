from django.urls import path
from . import views


app_name = "WH_share"
urlpatterns = [
    path('', views.ShareIndexView.as_view(), name="index"),
    path('list/', views.write_comment_view, name="write_comment_view")
]
