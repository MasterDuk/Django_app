from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Product
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start select field")
        users_info = User.objects.values_list("username", flat=True)
        print(list(users_info))
        for user_info in users_info:
            print(user_info)

        # products_values = Product.objects.values("pk", "name")
        # for p_values in products_values:
        #     print(p_values)

        self.stdout.write(f"Done")
