
import datetime
from email.policy import default
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.db.models.aggregates import Count
from django.db.models import F
from requests import request
from .forms import ArticleCreationForm, WriteCommentForm, ArticleSearchForm, ArticleEditForm
from .models import *
from .filters import ArticleFilter
# Create your views here.

from django.shortcuts import render

class MainPage(ListView):
    template_name = 'mainapp/index.html'
    model = Article
    context_object_name = 'articles'
    paginate_by = 2
    
    # def get(self, request, *args, **kwargs):
    #     period = self.request.GET.get('period')
    #     print(self.request.GET.get('period'))     
    
    def get_queryset(self):
        month_period = datetime.datetime.now(
            datetime.timezone.utc) - datetime.timedelta(days=2)
        week_period = datetime.datetime.now() - datetime.timedelta(days=7)

        queryset = ArticleFilter(
            self, articles=Article.objects.published()).run_filter()
            
        if self.request.GET.get('period'):
            period = self.request.GET.get('period')
            print(type(period))

            if period == '1':
                queryset = ArticleFilter(self, articles=Article.objects.published().annotate(likes_count=Count('likes')).order_by('-likes_count')).run_filter()

            elif period == '2':
                
                queryset = ArticleFilter(self, articles=Article.objects.published().filter(created_at__gt=month_period).annotate(
                likes_count=Count('likes')).order_by('-likes_count')
                ).run_filter()
                if queryset is None:
                    queryset=[]
                
            elif period == '3':
                queryset = ArticleFilter(self, articles=Article.objects.published().filter(created_at__gt=week_period).annotate(
                    likes_count=Count('likes')).order_by('-likes_count')).run_filter()
                if queryset is None:
                    queryset = []
                          
        return queryset
            
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_search_form'] = ArticleSearchForm()
        return context

class CategoryPage(ListView):
    model = Article
    template_name = 'mainapp/category_page.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        articles = Article.objects.published().filter(category__slug=self.kwargs.get(
            'category_slug')).select_related('category')
        if articles:
            articles = ArticleFilter(self, articles=articles).run_filter()
        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(
            slug=self.kwargs.get('category_slug')).first()
        context['title'] = category.title
        context['article_search_form'] = ArticleSearchForm()
        return context


class ShowArticle(View):

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        comments = Comment.objects.filter(article__pk=pk, parent=None).select_related('article').order_by('-created_at')
        comment_form = WriteCommentForm()
        return render(request, 'mainapp/exact_article.html', context={'article': article,'comments': comments,
        'comment_form': comment_form})
    
    def post(self, request, pk):
        if request.is_ajax():
            comment_form = WriteCommentForm(data=request.POST)
            if comment_form.is_valid():
                parent_id = request.POST.get("parent_id")
                if parent_id is not None:
                    new_reply = Comment.objects.create(article=Article.objects.filter(pk=pk).first(), parent = Comment.objects.filter(pk=parent_id).first(), body=comment_form.cleaned_data['body'], author = request.user)
                    new_reply.save()
                else:
                    new_comment = Comment.objects.create(article=Article.objects.filter(pk=pk).first(),
                    body=comment_form.cleaned_data['body'],
                    author = request.user)
                    new_comment.save()
                content = {'article': get_object_or_404(Article, pk=pk),
                        'comments': Comment.objects.filter(article__pk=pk, parent=None).select_related('article').order_by('-created_at')}
                result = render_to_string('mainapp/includes/comment.html', content)
                return JsonResponse({'result': result})  


def help_page(request):
    return render(request, 'help.html')


class CreateArticle(View):

    def get(self, request):
        create_form = ArticleCreationForm()
        context = {'create_form': create_form,
                   'title': 'Написать статью'}
        return render(request, 'mainapp/create_article.html', context=context)

    def post(self, request):
        create_form = ArticleCreationForm(request.POST)
        if create_form.is_valid():
            new_article = create_form.save(commit=False)
            new_article.text = request.POST.get('text')
            new_article.author = request.user
            new_article.save()
            create_form.save_m2m()
            return HttpResponsePermanentRedirect(reverse('main:main-page'))
        

class EditArticle(View):
    
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        edit_form = ArticleEditForm(initial={'title': article,
                                             'category': article.category,
                                             'text': article.text})
        context = {'edit_form': edit_form,
                   'article': article,
                   'title': 'Написать статью'}
        return render(request, 'mainapp/edit_article.html', context=context)
    
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        edit_form = ArticleEditForm(request.POST)
        if edit_form.is_valid():
            article.category = get_object_or_404(Category, title=edit_form.cleaned_data.get('category'))
            article.text = edit_form.cleaned_data.get('text')
            article.title = edit_form.cleaned_data.get('title')
            article.is_moderation = False
            article.save()
        return  HttpResponsePermanentRedirect(reverse('main:exact-article', kwargs={'pk': pk}))


class AddArticleLike(LoginRequiredMixin, View):

    def get_login_url(self):
        return 'user:signin'

    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, id=request.POST.get('article.id'))

        # Проверяем лайкал ли user эту статью
        if request.user not in article.likes.all():
            article.likes.add(request.user)
            
        else:
            messages.warning(request, "Вы уже отметили эту статью")
        
        request.session['vote'] = 1
        return HttpResponseRedirect(reverse('main:exact-article', args=[str(pk)]))


@method_decorator(csrf_exempt, name='dispatch')
class AddCommentLike(LoginRequiredMixin, View):

    def get_login_url(self):
        return 'user:signin'

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, id=request.POST.get('comment.id'))

        if request.user not in comment.likes.all():
            comment.likes.add(request.user)

        else:
            messages.info(request, "Вы уже отметили этот комментарий")

        request.session['vote'] = 2
        return HttpResponseRedirect(reverse('main:exact-article', args=[str(comment.article.id)]))


class AddArticleComplain(LoginRequiredMixin, View):

    def get_login_url(self):
        return 'user:signin'

    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, id=request.POST.get('article.id'))

        article.is_moderation = False
        article.save()

        return HttpResponseRedirect(reverse('main:exact-article', args=[str(pk)]))
