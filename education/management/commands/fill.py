from django.core.management import BaseCommand
from education.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = [
            {'student': 'Иванов Иван Иванович',
             'payment_date': '2023-11-15',
             'course': 'Python developer start',
             'lesson': 'Урок 1. Введение в профессию',
             'amount': 1000,
             'payment_form': 'cash'},
            {'student': 'Иванов Иван Иванович',
             'payment_date': '2023-11-20',
             'course': 'Python developer start',
             'lesson': 'Урок 2. Основы синтаксиса Python',
             'amount': 1000,
             'payment_form': 'cash'},
            {'student': 'Петров Петр Петрович',
             'payment_date': '2023-11-19',
             'course': 'Python developer start',
             'amount': 15000,
             'payment_form': 'remittance'},
            {'student': 'Богданов Петр Петрович',
             'payment_date': '2023-11-17',
             'course': 'Python developer pro',
             'amount': 40000,
             'payment_form': 'remittance'},
        ]

        payment_for_create = []
        for payment_item in payment_list:
            payment_for_create.append(
                Payment(**payment_item)
            )

        Payment.objects.all().delete()
        Payment.objects.bulk_create(payment_for_create)
