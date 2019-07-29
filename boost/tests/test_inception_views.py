from django.test import TestCase
from django.urls import reverse


class TestLoginRequired(TestCase):

    def test_redirects_to_login_page_search_view(self):
        response = self.client.get(reverse('search_form'))
        self.assertRedirects(response, f'{reverse("account_login")}?next=/search')

    def test_redirects_to_login_page_image_view(self):
        response = self.client.get(reverse('image_form'))
        self.assertRedirects(response, f'{reverse("account_login")}?next=/image')
