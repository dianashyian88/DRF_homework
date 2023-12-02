from celery import shared_task
from education.models import Subscription
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from users.models import User
import datetime


@shared_task
def send_mail_update_course(pk):
    list_subscription = Subscription.objects.filter(course=pk)
    for obj in list_subscription:
        send_mail(
            subject='Обновление материалов курсов',
            message=f'Обновлен курс {obj.course.name}. Скорее посмотрите изменения!!!',
            from_email=EMAIL_HOST_USER,
            recipient_list=[obj.student.email],
            fail_silently=False,
        )


def check_user():
    list_user = User.objects.all()
    for obj in list_user:
        now = datetime.datetime.now()
        if obj.last_login is not None:
            time_delta = (now - obj.last_login).days
            if time_delta > 30:
                obj.is_active = False
                obj.save()
        else:
            time_delta = (now - obj.date_joined).days
            if time_delta > 30:
                obj.is_active = False
                obj.save()
