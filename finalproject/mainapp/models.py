from django.db import models
from userapp.models import BaseUser

# Модель раздела/категории.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


# Модель статьи/публикации.
class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        BaseUser, on_delete=models.PROTECT)
    text = models.TextField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title



