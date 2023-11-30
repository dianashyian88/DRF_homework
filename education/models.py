from django.db import models
from config.settings import AUTH_USER_MODEL
from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    image = models.ImageField(upload_to='education/course/', verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name="цена", default=10000)

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
    price = models.PositiveIntegerField(verbose_name="цена", default=1000)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('id',)


class Payment(models.Model):
    PAYMENT_FORM_CHOICES = [
        ('cash', 'наличными'),
        ('remittance', 'перевод на счет'),
    ]
    student = models.CharField(max_length=100, verbose_name='ФИО', **NULLABLE)
    payment_date = models.DateField(verbose_name='дата платежа', auto_now_add=True, **NULLABLE)
    course = models.CharField(max_length=100, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.CharField(max_length=200, verbose_name='оплаченный урок', **NULLABLE)
    amount = models.FloatField(verbose_name='сумма платежа', default=0)
    payment_form = models.CharField(max_length=20, choices=PAYMENT_FORM_CHOICES,
                                    default='cash', verbose_name='форма оплаты')
    stripe_id = models.CharField(max_length=100, unique=True, **NULLABLE)
    status = models.CharField(max_length=150, verbose_name="статус", **NULLABLE)

    def __str__(self):
        return f'{self.student}, {self.payment_date}, {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('id',)


class Subscription(models.Model):
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='признак активной подписки')

    def __str__(self):
        return f'{self.student}, {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ('id',)
