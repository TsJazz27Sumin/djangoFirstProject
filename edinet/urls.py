from django.urls import path
from . import views

urlpatterns = [
    path('', views.corporate_officer_list, name='corporate_officer_list'),
    path('call-edinet-api', views.call_edinet_api, name='call_edinet_api'),
]