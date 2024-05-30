from random import choices
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Product
from shopapp.utils import add_two_numbers

# Create your tests here.

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        responce = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10"
            }
        )
        self.assertRedirects(responce, reverse("shopapp:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name )

class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def test_products(self):
        responce = self.client.get(reverse("shopapp:products_list"))
            # for product in Product.objects.filter(archived=False).all():
            #     self.assertContains(responce, product.name)
        # products = Product.objects.filter(archived=False).all()
        # products_ = responce.context["products"]
        # for p, p_ in zip(products, products_):
        #     self.assertEqual(p.pk, p_.pk)
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in responce.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(responce, 'shopapp/products-list.html')

class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.credentials = dict(username="bib_test", password="qwerty")
        # cls.user = User.objects.create_user(**cls.credentials)
        cls.user = User.objects.create_user(username="bib_test", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        # self.client.login(**self.credentials)
        self.client.force_login(self.user)

    def test_orders_view(self):
        responce = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(responce, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        responce = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(responce.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), responce.url)

class ProductExportViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    def test_get_products_view(self):
        responce = self.client.get(reverse('shopapp:products-export'))
        self.assertEqual(responce.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {'pk': product.pk,
             'name': product.name,
             'price': str(product.price),
             'archived': product.archived,
             }
             for product in products
        ]
        products_data = responce.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )
