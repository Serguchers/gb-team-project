from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def show_main(request):
    return render(request, '../templates/base.html')

def show_design(request):
    return render(request, '../templates/base.html')

def show_web_dev(request):
    return render(request, '../templates/base.html')

def show_mobile_dev(request):
    return render(request, '../templates/base.html')

def show_marketing(request):
    return render(request, '../templates/base.html')

def registration(request):
    return render(request, '../templates.base.html')

def signin(request):
    return render(request, '../templates.base.html')

def help_page(request):
    return render(request, '../templates.base.html')
