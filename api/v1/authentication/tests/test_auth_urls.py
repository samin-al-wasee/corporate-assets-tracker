from django.test import SimpleTestCase, TestCase, Client
from rest_framework.test import APIClient
from rest_framework.response import Response
from django.urls import reverse


class URLTests(SimpleTestCase):
    def url_maps_correct_view(self, mapped_view, target_url, args=None):
        mapped_url = reverse(mapped_view, args=args)
        self.assertEquals(mapped_url, target_url)

    def test_signup_url_maps_correct_view(self):
        self.url_maps_correct_view(
            mapped_view="authentication:signup", target_url="/api/v1/auth/signup/"
        )

    def test_activation_url_maps_correct_view(self):
        self.url_maps_correct_view(
            mapped_view="authentication:activation",
            target_url="/api/v1/auth/activate/abcdefghij/",
            args=["abcdefghij"],
        )

    def test_re_activation_url_maps_correct_view(self):
        self.url_maps_correct_view(
            mapped_view="authentication:resend-activation",
            target_url="/api/v1/auth/re-activation/",
        )
