from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class BaseUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4())
    email = models.EmailField(unique=True, blank=False)
    email_verified = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    MEMBERSHIP_NOVICE = 'Novice'
    MEMBERSHIP_MIDDLE = 'Middle'
    MEMBERSHIP_ADVANCED = 'Advanced'
    MEMBERSHIP_GURU = 'Guru'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_NOVICE, 'Novice'),
        (MEMBERSHIP_MIDDLE, 'Middle'),
        (MEMBERSHIP_ADVANCED, 'Advanced'),
        (MEMBERSHIP_GURU, 'Guru'),
    ]
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/', default='')
    membership = models.CharField(
        max_length=10, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_NOVICE)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=BaseUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=BaseUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
    
    def __str__(self):
        return f'{self.user.username}'
