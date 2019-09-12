from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files import File

from dreamy.forms import DreamyUserCreationForm


User = get_user_model()


class RegistrationFormTests(TestCase):
    """Class for testing the registration form"""

    def setUp(self):
        """Set up"""
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user = User.objects.create(username='test_user',
                                        bio='test bio shorter than 500 characters',
                                        avatar=self.file,
                                        password='test password')

    def test_register_valid_form(self):
        """Check if form is valid for valid data"""
        data = {'username': 'new_user',
                'password1': self.user.password,
                'password2': self.user.password,
                'bio': self.user.bio,
                'avatar': self.user.avatar}
        form = DreamyUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_invalid_form_existing_user(self):
        """Check if form is invalid for existing username"""
        data = {'username': self.user.username,
                'password1': self.user.password,
                'password2': self.user.password,
                'bio': self.user.bio,
                'avatar': self.user.avatar}
        form = DreamyUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], "A user with that username already exists.")

    def test_register_valid_form_missing_avatar(self):
        """Check if form is valid for blank avatar. A default is set through the view."""
        data = {'username': 'new_user',
                'password1': self.user.password,
                'password2': self.user.password,
                'bio': self.user.bio}
        form = DreamyUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_valid_form_missing_bio(self):
        """Check if form is valid for blank avatar."""
        data = {'username': 'new_user',
                'password1': self.user.password,
                'password2': self.user.password}
        form = DreamyUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_invalid_form_too_long_bio(self):
        """Check if form is valid for blank avatar"""
        data = {'username': 'new_user',
                'password1': self.user.password,
                'password2': self.user.password,
                'bio': ''.join(['a' for i in range(501)])}
        form = DreamyUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
