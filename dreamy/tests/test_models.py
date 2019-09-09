from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate

from dreamy.models import User, UserFollower


class UserTest(TestCase):
    """User creation-related tests"""

    def setUp(self):
        """Set up the user for testing"""
        user = User.objects.create(username='test_user')
        user.set_password('test_password')
        user.save()

    def test_user_exists(self):
        """Test the existence of the user created in setUp"""
        user = User.objects.get(username='test_user')
        self.assertIsNotNone(user)

    def test_username_correct(self):
        """Test the existence of the user created in setUp"""
        user = User.objects.get(username='test_user')
        self.assertIsNotNone(user.username, 'test_user')

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


class FollowersTest(TestCase):
    """Followers-related tests"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.user_1 = User.objects.create(username='1st_user', password='bartestpass')
        self.user_2 = User.objects.create(username='2nd_user', password='bartestpass')
        self.user_3 = User.objects.create(username='3rd_user', password='bartestpass')
        self.user_4 = User.objects.create(username='4th_user', password='bartestpass')

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
        """Test if user_5 follows nobody"""
        following = UserFollower.objects.filter(follower=self.user_1)
        self.assertEqual(following.count(), 0)
