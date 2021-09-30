from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='user_image', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18, blank=True, null=True)
    activation_key = models.CharField(max_length=128, blank=True, default=18)
    activation_key_expires = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_activation_key_expires(self):
        if now() + timedelta(hours=48):
            return False
        return True


class UserProfile(models.Model):

    MALE = 'М'
    FEMALE = 'Ж'
    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж')
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='Тэги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='О себе', blank=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=5)

    @receiver(post_save,sender=User)
    def save_user_profile(sender,instance,**kwargs):
        instance.userprofile.save()
