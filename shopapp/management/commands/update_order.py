from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    '''
    Update order
    '''

    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
           self.stdout.write(f"No order found")

        products = Product.objects.all()

        for product in products:
            order.product.add(product)

        order.save()

        self.stdout.write(f"Successfully added products {order.product.all()} to order {order}")
