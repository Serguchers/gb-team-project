from django.urls import path
from .views import *
from .apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('main/', show_main, name='main-page'),
    path('design/', show_design),
    path('web-dev/', show_web_dev),
    path('mobile-dev/', show_mobile_dev),
    path('marketing/', show_marketing),
    path('help/', help_page),
    path('create-article/', create_article, name='create-article')
]