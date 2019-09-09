from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from os.path import join

from dreamy import APP_NAME
from dreamy.models import User, UserFollower


class HomePageTests(SimpleTestCase):
    """Class for testing home page view"""

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


class BrowseUsersTests(TestCase):
    """Class for testing browse_users view"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.user_1 = User.objects.create(username='1st_user', password='bartestpass')
        self.user_2 = User.objects.create(username='2nd_user', password='bartestpass')
        self.user_3 = User.objects.create(username='3rd_user', password='bartestpass')
        self.user_4 = User.objects.create(username='4th_user', password='bartestpass')

        self.users = [self.user_1, self.user_2, self.user_3, self.user_4]

    def test_browse_all_users_status_code(self):
        """Test if getting the browse_users page gives HTTP status code 200"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_browse_all_users_url_by_name(self):
        """Test if getting the browse_users page via the URL name gives HTTP status code 200"""
        response = self.client.get(reverse('browse_users'))
        self.assertEqual(response.status_code, 200)

    def test_browse_all_users_correct_template(self):
        """Test if URL 'browse_users' uses browse_users.html"""
        response = self.client.get(reverse('browse_users'))
        self.assertTemplateUsed(response, join(APP_NAME, 'browse_users.html'))

    def test_browse_all_users_contains_correct_html(self):
        """Test if URL 'browse_users' returns HTML with 'Browse Users'"""
        response = self.client.get(reverse('browse_users'))
        self.assertContains(response, '<h2>Browse users:</h2>')

    def test_browse_all_users_correct_user_links(self):
        """Test if URL 'browse_users' returns the correct user links"""
        response = self.client.get(reverse('browse_users'))
        for user in self.users:
            url = reverse('profile', kwargs={'user_id': user.id})
            self.assertContains(response, f'<a href="{url}">')


class BrowseFollowersTests(TestCase):
    """Class for testing browse_follows view for followers"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.user_1 = User.objects.create(username='1st_user', password='bartestpass')
        self.user_2 = User.objects.create(username='2nd_user', password='bartestpass')
        self.user_3 = User.objects.create(username='3rd_user', password='bartestpass')
        self.user_4 = User.objects.create(username='4th_user', password='bartestpass')

        self.users = [self.user_1, self.user_2, self.user_3, self.user_4]

        UserFollower.objects.create(user=self.user_1, follower=self.user_2)
        UserFollower.objects.create(user=self.user_1, follower=self.user_3)
        UserFollower.objects.create(user=self.user_1, follower=self.user_4)

        UserFollower.objects.create(user=self.user_2, follower=self.user_3)

    def test_browse_followers_status_code(self):
        """Test if getting the browse_users page gives HTTP status code 200 for user_1's followers"""
        response = self.client.get(f'/users/{self.user_1.id}/followers/')
        self.assertEqual(response.status_code, 200)

    def test_browse_followers_url_by_name(self):
        """Test if getting the browse_follows page via the URL name gives HTTP status code 200 for user_1's followers"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'followers'}))
        self.assertEqual(response.status_code, 200)

    def test_browse_followers_correct_template(self):
        """Test if URL 'browse_follows' uses browse_users.html for user_1's followers"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'followers'}))
        self.assertTemplateUsed(response, join(APP_NAME, 'browse_users.html'))

    def test_browse_followers_contains_correct_html(self):
        """Test if URL 'browse_follows' returns HTML with 'Browse 1st_user's followers"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'followers'}))
        self.assertContains(response, f"<h2>Browse {self.user_1.username}&#39;s followers:</h2>")

    def test_browse_followers_correct_user_links(self):
        """Test if URL 'browse_follows' returns the correct user links"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'followers'}))
        followers = [uf.follower for uf in UserFollower.objects.filter(user=self.user_1)]
        for follower in followers:
            url = reverse('profile', kwargs={'user_id': follower.id})
            self.assertContains(response, f'<a href="{url}">')


class BrowseFollowingTests(TestCase):
    """Class for testing browse_follows view for followees"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.user_1 = User.objects.create(username='1st_user', password='bartestpass')
        self.user_2 = User.objects.create(username='2nd_user', password='bartestpass')
        self.user_3 = User.objects.create(username='3rd_user', password='bartestpass')
        self.user_4 = User.objects.create(username='4th_user', password='bartestpass')

        self.users = [self.user_1, self.user_2, self.user_3, self.user_4]

        UserFollower.objects.create(user=self.user_1, follower=self.user_2)
        UserFollower.objects.create(user=self.user_1, follower=self.user_3)
        UserFollower.objects.create(user=self.user_1, follower=self.user_4)

        UserFollower.objects.create(user=self.user_2, follower=self.user_3)

    def test_browse_following_status_code(self):
        """browse_follows page gives HTTP status code 200 for users user_1 is following"""
        response = self.client.get(f'/users/{self.user_1.id}/following/')
        self.assertEqual(response.status_code, 200)

    def test_browse_following_url_by_name(self):
        """browse_follows page for users user_1 is following via the URL name gives HTTP status code 200"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'following'}))
        self.assertEqual(response.status_code, 200)

    def test_browse_following_correct_template(self):
        """Test if URL 'browse_follows' uses browse_users.html for users user_1 is following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'following'}))
        self.assertTemplateUsed(response, join(APP_NAME, 'browse_users.html'))

    def test_browse_following_contains_correct_html(self):
        """Test if URL 'browse_follows' returns HTML with 'Browse 1st_user's following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'following'}))
        self.assertContains(response, f"<h2>Browse users {self.user_1.username} follows:</h2>")

    def test_browse_following_correct_user_links(self):
        """Test if URL 'browse_follows' returns the correct user links for users user_3 is following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_3.id, 'follow': 'following'}))
        following = [uf.user for uf in UserFollower.objects.filter(follower=self.user_3)]
        for follower in following:
            url = reverse('profile', kwargs={'user_id': follower.id})
            self.assertContains(response, f'<a href="{url}">')


class RegistrationTests(TestCase):
    """Class for testing the registration view"""

    pass


class UserProfileTests(TestCase):
    """Class for testing the user profile"""

    def setUp(self):
        self.user_1 = User.objects.create(username='test_user')
        self.user_1.set_password('test_password')
        self.user_1.bio = "test_bio"
        self.user_1.save()

    def test_profile_status_code(self):
        """browse_follows page gives HTTP status code 200 for users user_1 is following"""
        response = self.client.get(f'/users/{self.user_1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_by_name(self):
        """browse_follows page for users user_1 is following via the URL name gives HTTP status code 200"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertEqual(response.status_code, 200)

    def test_profile_correct_template(self):
        """Test if URL 'browse_follows' uses browse_users.html for users user_1 is following"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertTemplateUsed(response, join(APP_NAME, 'profile.html'))

    def test_profile_contains_correct_html(self):
        """Test if URL 'browse_follows' returns HTML with 'Browse 1st_user's following"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertContains(response, f"<h2>{self.user_1.username}</h2>")
