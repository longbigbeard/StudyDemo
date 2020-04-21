from django.urls import path
from . import views

app_name = 'WH_auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('img_captcha/', views.img_captcha, name='img_captcha'),
    path('register/', views.register, name='register'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('edit_author_info/', views.edit_author_info, name='edit_author_info'),
    path('edit_order/', views.edit_order, name='edit_order'),
    path('edit_order_info/', views.edit_order_info, name='edit_order_info'),
    path('edit_share/', views.edit_share, name='edit_share'),
    path('edit_share_info/', views.edit_share_info, name='edit_share_info'),
]
