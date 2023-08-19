from django.urls import reverse
from django.test import TestCase


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        # print(self.client.get(reverse("myauth:cookie-get")))
        response = self.client.get(reverse("myauth:cookie-get"))
        self.assertContains(response, "Cookie")


class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse("myauth:foo-bar"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.headers["content-type"], "application/json"
        )
        expected_data = {"foo": "bar", "spam": "eggs"}
        self.assertJSONEqual(response.content, expected_data)

