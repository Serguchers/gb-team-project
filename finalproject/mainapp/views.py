from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import ArticleCreationForm
from .models import *
# Create your views here.

from django.shortcuts import render


def show_main(request):
    articles = Article.objects.select_related('category').order_by('created_at')
    return render(request, 'index.html', context={
        'articles': articles
    })

def show_design(request):
    return render(request, 'design.html')

def show_web_dev(request):
    return render(request, 'web_dev.html')

def show_mobile_dev(request):
    return render(request, 'mobile_dev.html')

def show_marketing(request):
    return render(request, 'marketing.html')

def registration(request):
    return render(request, 'registration.html')


def signin(request):
    return render(request, '../templates.base.html')

def help_page(request):
    return render(request, 'help.html')


def create_article(request):
    if request.method == 'POST':
        create_form = ArticleCreationForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponsePermanentRedirect(reverse('main:main-page'))
    else:
        create_form = ArticleCreationForm()
        
    context = {'create_form': create_form}
    return render(request, 'create_article.html', context=context)