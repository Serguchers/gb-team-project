from datetime import date
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from userapp.models import BaseUser, UserProfile
from userapp.utils import send_verifying_email


year = date.today().year


class BaseUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Логин'})
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Почта'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='Повторите Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'password1', 'password2']


class SigninUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Логин'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Пароль'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

            if not self.user_cache.email_verified:
                send_verifying_email(self.request, self.user_cache)
                raise forms.ValidationError(
                    'Ваша почта не верифицирована. Проверьте почту',
                    code='invalid login'
                )     

        else:
            return self.cleaned_data




class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    birth_date = forms.DateField(required=True,
                                 widget=forms.SelectDateWidget(
                                     years=range(year, year-101, -1)
                                 ))

    avatar = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['birth_date', 'avatar']


# class MyPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(
#         label="Email",
#         widget=forms.EmailInput(attrs={'autocomplete': 'email',
#                                        'class': 'form-control',
#                                        'placeholder': 'Повторите пароль'
#                                        })
#     )
#
#     class Meta:
#         model = BaseUser
#         fields = ['email']
