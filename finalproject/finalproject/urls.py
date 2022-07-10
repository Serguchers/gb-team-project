"""finalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp




urlpatterns = [
    path('', mainapp.show_main),
    path('design/', mainapp.show_design),
    path('web-dev/', mainapp.show_web_dev),
    path('mobile-dev/', mainapp.show_mobile_dev),
    path('marketing/', mainapp.show_marketing),
    path('registration/', mainapp.registration),
    path('signin/', mainapp.signin),
    path('admin', admin.site.urls),
    path('help/', mainapp.help_page),
]
