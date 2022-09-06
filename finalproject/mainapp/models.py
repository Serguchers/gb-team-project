from django.db import models
from pytils.translit import slugify
from userapp.models import BaseUser
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

# Модель раздела/категории.

class Category(models.Model):
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class ArticlesQuerySet(models.QuerySet):

    def published(self):
        return self.filter(is_published=True)
    
    def not_published(self):
        return self.filter(is_published=False)

    def not_moderation(self):
        return self.filter(is_moderation=False)


class ActiveArticlesManager(models.Manager):
    def get_queryset(self):
        return ArticlesQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()
    
    def not_published(self):
        return self.get_queryset().not_published()

    def not_moderation(self):
        return self.get_queryset().not_moderation()


# Модель статьи/публикации.
class Article(models.Model):
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        BaseUser, on_delete=models.PROTECT, default=None)
    text = RichTextField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_moderation = models.BooleanField(default=False)
    # Теги для статей
    tags = TaggableManager()
    likes = models.ManyToManyField(BaseUser, blank=True, related_name='article_likes')
    
    objects = ActiveArticlesManager()

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title}-{self.author.username}')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


# Комментарий
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        BaseUser, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField(blank=False, null=False)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(
        BaseUser, blank=True, related_name='comment_likes')

    def children(self):
        return Comment.objects.filter(parent=self)
        
    def __str__(self):
        return f'{self.body}'
    
