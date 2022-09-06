from django.urls import path
from .views import *
from .apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),
    path('category/<slug:category_slug>/', CategoryPage.as_view(), name='category'),
    path('help/', help_page),
    path('create-article/', CreateArticle.as_view(), name='create-article'),
    path('article/<pk>/', ShowArticle.as_view(), name='exact-article'),
    path('edit/<pk>/', EditArticle.as_view(), name='edit-article'),
    path('article/<int:pk>/like', AddArticleLike.as_view(), name='article-like'),
    path('comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('article/<int:pk>/complain', AddArticleComplain.as_view(), name='article-complain'),
]