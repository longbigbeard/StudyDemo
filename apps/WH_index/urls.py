from django.urls import path
from . import views

app_name = 'WH_index'

urlpatterns = [
   path('', views.index, name='index'),
   path('attention/', views.attention, name='attention')
]

