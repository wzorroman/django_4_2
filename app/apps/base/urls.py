from django.urls import path
from . import views
from .views import views_base, view_cotizador

app_name = 'base'

urlpatterns = [
    path('inicio', views.index, name='app_base'),
    path('demo', views_base.IndexBlankView.as_view(), name='demo1'),
    path('', view_cotizador.CotizadorDemoView.as_view(), name='cotizador'),
    path('cronograma', view_cotizador.CronogramaReporte.as_view(), name='cronograma'),
    

]