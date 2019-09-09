from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from os.path import join

from dreamy import views, APP_NAME
from dreamy.models import User


class HomePageTests(SimpleTestCase):
    """Class for testing views"""

    def test_home_page_status_code(self):
        """Test if getting the home page gives HTTP status code 200"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_by_name(self):
        """Test if getting the home page via the URL namegives HTTP status code 200"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_correct_template(self):
        """Test if URL 'home' uses index.html"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, join(APP_NAME, 'index.html'))

    def test_home_contains_correct_html(self):
        """Test if URL 'home' uses index.html"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<h2>Home</h2>')


class LoginRedirectTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='test_user', password='test_password')
        pass
