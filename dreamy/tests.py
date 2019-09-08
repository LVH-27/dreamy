from django.test import TestCase
from django.contrib.auth import get_user_model


UserObject = get_user_model()


class UserCreateTest(TestCase):
    """User creation-related tests"""

    def setUp(self):
        """Set up the user for testing"""
        UserObject.objects.create(username='foo', password='bartestpass')

    def test_user_exists(self):
        """Test the existence of the user created in SetUp"""
        user = UserObject.objects.get(username='foo')
        self.assertIsNotNone(user.username, 'foo')
