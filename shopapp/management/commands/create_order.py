from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    """
    Create order
    """

    # def handle(self, *args, **options):
    #     self.stdout.write("Create order")
    #     user = User.objects.get(username='admin')
    #     order = Order.objects.get_or_create(
    #         delivery_address = "ul. Novay, d 15",
    #         promocode = "SALE123",
    #         user=user,
    #     )
    #     self.stdout.write(f"Created order {order}")
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create order with product")
        user = User.objects.get(username='admin')
        # products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()  # исключаются поля
        products: Sequence[Product] = Product.objects.only("id").all()
        order, created = Order.objects.get_or_create(
            delivery_address="ul. Starppy, d 8",
            promocode="promo9",
            user=user,
        )
        for product in products:
            order.product.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")
