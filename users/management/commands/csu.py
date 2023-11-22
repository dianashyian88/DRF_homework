from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='adminDS@mail.ru',
            username='Суханова Диана Владимировна',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('123456qwerty')
        user.save()
