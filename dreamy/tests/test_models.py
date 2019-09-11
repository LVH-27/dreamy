from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.core.files import File
from django.core.exceptions import ValidationError

from dreamy.models import User, UserFollower, Post


class UserTests(TestCase):
    """User creation-related tests"""

    def setUp(self):
        """Set up the user for testing"""
        user = User.objects.create(username='test_user')
        user.set_password('test_password')
        file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        user.avatar.save('default_avatar.png', file)
        user.save()

    def test_user_exists(self):
        """Test the existence of the user created in setUp"""
        user = User.objects.get(username='test_user')
        self.assertIsNotNone(user)

    def test_username_correct(self):
        """Test the existence of the user created in setUp"""
        user = User.objects.get(username='test_user')
        self.assertIsNotNone(user.username, 'test_user')

    def test_user_has_avatar(self):
        user = User.objects.get(username='test_user')
        self.assertTrue(user.avatar)

    def test_user_username_none_fails(self):
        """Test if users with username set to None can be saved"""
        user = User.objects.get(username='test_user')
        user.username = None
        self.assertRaises(IntegrityError, user.save)

    def test_user_successful_authentication(self):
        """Test if authentication succeeds with correct credentials"""
        user = authenticate(username='test_user', password='test_password')
        self.assertIsNotNone(user)

    def test_user_unsuccessful_authentication(self):
        """Test if authentication fails with wrong credentials"""
        user = authenticate(username='test_user', password='incorrect_password')
        self.assertIsNone(user)


class FollowersTests(TestCase):
    """Followers-related tests"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='user_1', password='bartestpass', avatar=self.file)
        self.user_2 = User.objects.create(username='user_2', password='bartestpass', avatar=self.file)
        self.user_3 = User.objects.create(username='user_3', password='bartestpass', avatar=self.file)
        self.user_4 = User.objects.create(username='user_4', password='bartestpass', avatar=self.file)

        UserFollower.objects.create(user=self.user_1, follower=self.user_2)
        UserFollower.objects.create(user=self.user_1, follower=self.user_3)
        UserFollower.objects.create(user=self.user_1, follower=self.user_4)

        UserFollower.objects.create(user=self.user_2, follower=self.user_3)

    def test_followers_correct(self):
        """Test if user_1 has followers user_2, user_3 and user_4"""
        followers = [uf.follower for uf in UserFollower.objects.filter(user=self.user_1)]
        self.assertTrue(self.user_2 in followers and self.user_3 in followers and self.user_4 in followers)

    def test_following_correct(self):
        """Test if user_3 follows 2 users (user_1 and user_2)"""
        following = [uf.user for uf in UserFollower.objects.filter(follower=self.user_3)]
        self.assertTrue(self.user_1 in following and self.user_2 in following)

    def test_followers_none_correct(self):
        """Test if user_3 has no followers"""
        followers = UserFollower.objects.filter(user=self.user_3)
        self.assertEqual(followers.count(), 0)

    def test_following_none_correct(self):
        """Test if user_1 follows nobody"""
        following = UserFollower.objects.filter(follower=self.user_1)
        self.assertEqual(following.count(), 0)

    def test_user_follower_repr_correct(self):
        """Test if __repr__ for UserFollower works correctly"""
        uf = UserFollower.objects.get(user=self.user_1, follower=self.user_2)
        self.assertEqual(uf.__repr__(), f"<User {self.user_1.username} - Follower {self.user_2.username}>")


class PostTests(TestCase):
    """Post-related tests"""

    def setUp(self):
        """Create posts, users and followers for testing"""
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='user_1', password='bartestpass', avatar=self.file)

        self.post = Post(
            description='test description shorter than 300 characters',
            author=self.user_1,
            image=self.file)

    def test_post_correct_author(self):
        """Test if the post's author is correct."""
        self.assertEqual(self.post.author, self.user_1)

    def test_post_fail_description_more_than_300(self):
        """Test if validation fails for descriptions longer than 300 characters."""
        self.post.description = ''.join(['a' for i in range(301)])
        self.assertRaises(ValidationError, self.post.full_clean)

    def test_post_fail_without_description(self):
        """Test if validation fails for blank descriptions."""
        self.post.description = ''
        self.assertRaises(ValidationError, self.post.full_clean)

    def test_post_fail_without_image(self):
        """Test if validation fails for posts with no image."""
        self.post.image = None
        self.assertRaises(ValidationError, self.post.full_clean)
