from django import forms
from django.core.exceptions import ValidationError
from .models import Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from userapp.models import BaseUser
from ckeditor.widgets import CKEditorWidget


class ArticleCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=100,
                            required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn  dropdown-toggle {{ category }}'}))
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ('title', 'category', 'tags')

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < 100:
            raise ValidationError("Текст слишком короткий!")
        return data

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 8:
            raise ValidationError("Слишком короткое название")
        return data
    

class ArticleEditForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ('title', 'category')

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < 100:
            raise ValidationError("Текст слишком короткий!")
        return data

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 8:
            raise ValidationError("Слишком короткое название")
        return data


class WriteCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'comment-area form-control shadow-sm',
               'rows': '3'}), required=True)


class ArticleSearchForm(forms.Form):
    ORDER_CHOICES = (
        ('', ''),
        ('-created_at', 'Сначала новые'),
        ('created_at', 'Сначала старые')
    )

    title = forms.CharField(required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Поиск'}))
    tags = forms.CharField(required=False)
    created_order = forms.ChoiceField(choices=ORDER_CHOICES, required=False)
