from django.test import TestCase
from django.contrib.auth.models import User


class UserCreateTest(TestCase):
    """User creation-related tests"""

    def setUp(self):
        """Set up the user for testing"""
        User.objects.create(username='foo', password='bartestpass')

    def test_user_exists(self):
        """Test the existence of the user created in SetUp"""
        user = User.objects.get(username='foo')
        self.assertIsNotNone(user.username, 'foo')
