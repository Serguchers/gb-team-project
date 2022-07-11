from django.shortcuts import render


# Create your views here.

from django.shortcuts import render


def show_main(request):
    return render(request, 'index.html')

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

