from django.urls import path
from . import views

app_name = 'WH_order'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_order/', views.new_order, name='new_order'),
    path('pay_order/', views.pay_order, name='pay_order'),
    path('<order_id>/', views.paying_order, name='paying_order'),

]
