from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout, update_session_auth_hash, login, authenticate
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.core.exceptions import ValidationError

from userapp.utils import send_verifying_email
from .forms import BaseUserCreationForm, SigninUserForm, UpdateUserForm,\
    UpdateProfileForm
from mainapp.models import Article
from .models import BaseUser

# Create your views here.


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user)
            return redirect('main:main-page')
        return redirect('user:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = BaseUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                BaseUser.DoesNotExist, ValidationError):
            user = None
        return user


class RegisterUser(View):
    template_name = 'userapp/registration.html'

    def get(self, request):
        context = {
            'form': BaseUserCreationForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = BaseUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,
                                email=email, password=password)
            send_verifying_email(request, user)
            return redirect('user:confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class LoginUser(LoginView):
    form_class = SigninUserForm
    template_name = 'userapp/signin.html'

    def get_success_url(self):
        try:
            redicrect_way = self.request.GET.get('next')
            redicrect_way = redicrect_way.split('/')
            redicrect_way.pop(-1)
            redicrect_way = '/'.join(redicrect_way)
            return redicrect_way
        except:
            return reverse_lazy('main:main-page')


def signout_user(request):
    logout(request)
    return redirect('main:main-page')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                         request.FILES,
                                         instance=request.user.userprofile
                                         )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.userprofile)

    return render(request, 'userapp/profile.html', {'user_form': user_form,
                                                    'profile_form': profile_form})


@login_required
def my_article(request):
    articles = Article.objects.filter(
        author_id__username=request.user)\
        .select_related('author').order_by(
        '-created_at')
    return render(request, 'userapp/my_article.html'
                  , context={'articles': articles}
                  )


@login_required
def password_reset_by_user(request):
   form = PasswordChangeForm(user=request.user, data=request.POST or None)
   if form.is_valid():
     form.save()
     update_session_auth_hash(request, form.user)
     return redirect('/')
   return render(request, 'userapp/change_password.html', {'form': form})


def get_user_profile(request, username):
    user = get_object_or_404(BaseUser, username=username)
    profile_form = user.userprofile
    articles = Article.objects.filter(
        author_id__username=user) \
        .select_related('author').order_by(
        '-created_at')
    return render(request, 'userapp/user_profile.html', {'user': user,
                                                         'articles': articles,
                                                         'profile_form': profile_form
                                                         })
