from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth import views
from .views import *
from .apps import UserappConfig

app_name = UserappConfig.name

urlpatterns = [
    path('signin/', LoginUser.as_view(), name='signin'),
    path('', include('django.contrib.auth.urls')),
    path('signout/', signout_user, name='signout'),
    path('profile/', profile, name='profile'),
    path('my-article/', my_article, name='my_article'),
    path('password-change/', password_reset_by_user,
         name='change_password'),
    path('confirm_email/',
         TemplateView.as_view(template_name='userapp/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(),
         name='verify_email'),
    path('invalid_verify/',
        TemplateView.as_view(template_name='userapp/invalid_verify.html'),
        name='invalid_verify'),
    path('registration/', RegisterUser.as_view()),

    path('pass_reset/', views.PasswordResetView.as_view(
        success_url='/pass_reset/done/',
        email_template_name='userapp/registrations/my_password_reset_email.html',
        template_name='userapp/registrations/my_password_reset.html'
    ), name='pass_reset'),
    path('pass_reset/done/', views.PasswordResetDoneView.as_view(
        template_name='userapp/registrations/my_password_reset_done.html'
    ), name='pass_reset_done'),
    path('res/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        success_url='/res/done/',
        template_name='userapp/registrations/my_password_reset_confirm.html'
    ), name='pass_reset_confirm'),
    path('res/done/', views.PasswordResetCompleteView.as_view(
        template_name='userapp/registrations/my_password_reset_complete.html'
    ), name='pass_reset_complete'),
    path('users/<username>/', get_user_profile, name='exact-user-profile')
]
