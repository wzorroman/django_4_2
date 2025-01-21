from django.urls import path
from . import views
from .views import views_base

app_name = 'base'

urlpatterns = [
    path('', views.index, name='app_base'),
    path('demo', views_base.IndexBlankView.as_view(), name='demo1'),
]