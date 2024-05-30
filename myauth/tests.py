import json
from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        responce = self.client.get(reverse("myauth:cookie-get"))
        self.assertContains(responce, "Cookie value")


class FooBarViewTest(TestCase):
    def test_foo_bar_view(self):
        responce = self.client.get(reverse("myauth:foo-bar"))
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(
            responce.headers['content-type'], 'application/json',
        )
        expected_data = {"foo": "bar", "spam": "eggs"}
        # received_data = json.loads(responce.content)
        # self.assertEqual(received_data, expected_data)
        self.assertJSONEqual(responce.content, expected_data)
