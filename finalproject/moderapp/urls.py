from django.urls import path
from .views import *
from .apps import  ModerappConfig

app_name = ModerappConfig.name

urlpatterns = [
    path('approve-articles/', ArticlesToApprove.as_view(), name='articles-to-approve'),
    path('approve-or-block/<int:pk>/', ApproveOrBlock.as_view(), name='approve-or-block'),
    path('ban-user/<username>/', BanUser.as_view(), name='ban-page'),
    path('banned/', Banned.as_view(), name='banned')
]