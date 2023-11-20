from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    STATUS_USER_CHOICES = [
        ('owner', 'владелец курса'),
        ('student', 'студент'),
    ]
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=40, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    email_verify = models.BooleanField(default=False)
    status_user = models.CharField(max_length=20, choices=STATUS_USER_CHOICES,
                                   default='student', verbose_name='статус пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
