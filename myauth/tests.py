from django.urls import reverse
from django.test import TestCase


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        # print(self.client.get(reverse("myauth:cookie-get")))
        response = self.client.get(reverse("myauth:cookie-get"))
        self.assertContains(response, "value")
