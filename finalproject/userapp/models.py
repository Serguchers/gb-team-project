from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class BaseUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4())
    email = models.EmailField(unique=True, blank=False)
    
    def __str__(self):
        return self.username