from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from mainapp.models import Article 
from mainapp.filters import ArticleFilter
from mainapp.forms import ArticleSearchForm
from userapp.models import BaseUser
# Create your views here.

@method_decorator(staff_member_required, name='dispatch')
class ArticlesToApprove(LoginRequiredMixin, ListView):
    template_name = 'moderapp/articles_to_approve.html'
    model = Article
    context_object_name = 'articles'
    
    def get_queryset(self):
        articles = Article.objects.all()
        return articles
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_search_form'] = ArticleSearchForm()
        return context


@method_decorator(staff_member_required, name='dispatch')
class UsersToApprove(LoginRequiredMixin, ListView):
    template_name = 'moderapp/articles_to_approve.html'
    model = BaseUser
    context_object_name = 'users'

    def get_queryset(self):
        users = BaseUser.objects.all()
        return users

    

@method_decorator(staff_member_required, name='dispatch')
class ApproveOrBlock(View):

    def post(self, request, pk):
        if request.POST.get('approve'):
            article = get_object_or_404(Article, pk=pk)
            article.is_published = True
            article.is_moderation = True
            article.save()
        if request.POST.get('block'):
            article = get_object_or_404(Article, pk=pk)
            article.is_published = False
            article.is_moderation = True
            article.save()

        return HttpResponseRedirect(reverse('moder:articles-to-approve'))
    
    
@method_decorator(staff_member_required, name='dispatch')
class BanUser(View):
    def post(self, request, username):
        user = get_object_or_404(BaseUser, username=username)
        if user.is_banned:
            user.is_banned = False
        else:
            user.is_banned = True
        user.save()
        # return HttpResponseRedirect(reverse('mainapp:main-page'))
        return HttpResponseRedirect(reverse('userapp:exact-user-profile', kwargs={'username': user.username}))
    

class Banned(TemplateView):
    template_name = 'moderapp/banned_page.html'