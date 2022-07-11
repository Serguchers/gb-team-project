from django.db import models

# Модель пользователя.
# Закомментировал пока поле АВАТАР,
# т.к. требует доп настроек (сделаем потом)
class User(models.Model):
    user_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # avatar = models.ImageField(upload_to='images') # это папка под имиджи 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user_name


# Модель раздела/категории.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


# Модель статьи/публикации.
class Articles(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title



