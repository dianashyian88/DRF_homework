from django.db import models
from config.settings import AUTH_USER_MODEL
from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    image = models.ImageField(upload_to='education/course/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('id',)


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    image = models.ImageField(upload_to='education/lesson/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    link_to_video = models.URLField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('id',)
