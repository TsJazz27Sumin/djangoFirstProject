from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('call-edinet-api', views.call_edinet_api, name='call_edinet_api'),
    path('reload', views.reload, name='reload'),
    path('try-ajax', views.try_ajax, name='try_ajax'),
]