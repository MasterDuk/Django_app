from typing import Sequence

from django.core.management import BaseCommand
from django.db.models import Avg, Max, Min, Count, Sum

from shopapp.models import Product, Order
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start aggregate")

        # result = Product.objects.filter(
        #     name__contains="Smartphone",
        # ).aggregate(
        #     Avg("price"),
        #     Max("price"),
        #     min_price=Min("price"),
        #     count=Count("id"),
        # )
        # print(result)
        orders = Order.objects.annotate(
            total=Sum("product__price", default=0),
            product_count=Count("product"),
        )
        for order in orders:
            print(
                f"Order #{order.id} "
                f"with {order.product_count} "
                f"product worth {order.total} "
            )
        self.stdout.write(f"Done")