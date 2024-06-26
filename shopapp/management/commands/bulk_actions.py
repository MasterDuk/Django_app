from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start bulk")

        # обновление записи
        result = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)
        print(result)

        # вставка записи
        # info = [
        #     ('Smartphone 1', 199),
        #     ('Smartphone 2', 299),
        #     ('Smartphone 3', 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write(f"Done")