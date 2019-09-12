from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.core.files import File
from django.contrib.auth import get_user_model

from os.path import join, basename
import re

from dreamy import APP_NAME
from dreamy.models import UserFollower, Post


User = get_user_model()


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
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='user_1', password='bartestpass', avatar=self.file)
        self.user_2 = User.objects.create(username='user_2', password='bartestpass', avatar=self.file)
        self.user_3 = User.objects.create(username='user_3', password='bartestpass', avatar=self.file)
        self.user_4 = User.objects.create(username='user_4', password='bartestpass', avatar=self.file)

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
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='user_1', password='bartestpass', avatar=self.file)
        self.user_2 = User.objects.create(username='user_2', password='bartestpass', avatar=self.file)
        self.user_3 = User.objects.create(username='user_3', password='bartestpass', avatar=self.file)
        self.user_4 = User.objects.create(username='user_4', password='bartestpass', avatar=self.file)
        self.user_5 = User.objects.create(username='user_5', password='bartestpass', avatar=self.file)

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
        """Test if URL 'browse_follows' returns HTML with 'Browse user_1's followers"""
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

    def test_browse_followers_not_contains_not_followers_user_links(self):
        """Test if URL 'browse_follows' returns only the correct user links for user_1's followers"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'followers'}))
        # using set instead of list to get rid of duplicates
        all_users = set(User.objects.all())
        followers = {uf.follower for uf in UserFollower.objects.filter(user=self.user_1)}
        not_followers = all_users.difference(followers)

        if self.user_1 in not_followers:
            # self.user_1 must be removed if present because the view rightly contains a link to their profile
            not_followers.remove(self.user_1)

        for user in not_followers:
            url = reverse('profile', kwargs={'user_id': user.id})
            self.assertNotContains(response, f'<a href="{url}">')


class BrowseFollowingTests(TestCase):
    """Class for testing browse_follows view for followees"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='user_1', password='bartestpass', avatar=self.file)
        self.user_2 = User.objects.create(username='user_2', password='bartestpass', avatar=self.file)
        self.user_3 = User.objects.create(username='user_3', password='bartestpass', avatar=self.file)
        self.user_4 = User.objects.create(username='user_4', password='bartestpass', avatar=self.file)

        self.users = [self.user_1, self.user_2, self.user_3, self.user_4]

        UserFollower.objects.create(user=self.user_1, follower=self.user_2)
        UserFollower.objects.create(user=self.user_1, follower=self.user_3)
        UserFollower.objects.create(user=self.user_1, follower=self.user_4)

        UserFollower.objects.create(user=self.user_2, follower=self.user_3)

    def test_browse_following_status_code(self):
        """'browse_follows' page gives HTTP status code 200 for users user_1 is following"""
        response = self.client.get(f'/users/{self.user_1.id}/following/')
        self.assertEqual(response.status_code, 200)

    def test_browse_following_url_by_name(self):
        """'browse_follows' page for users user_1 is following via the URL name gives HTTP status code 200"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'following'}))
        self.assertEqual(response.status_code, 200)

    def test_browse_following_correct_template(self):
        """Test if URL 'browse_follows' uses browse_users.html for users user_1 is following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'following'}))
        self.assertTemplateUsed(response, join(APP_NAME, 'browse_users.html'))

    def test_browse_following_contains_correct_html(self):
        """Test if URL 'browse_follows' returns HTML with 'Browse user_1's following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_1.id, 'follow': 'following'}))
        self.assertContains(response, f"<h2>Browse users {self.user_1.username} follows:</h2>")

    def test_browse_following_contains_correct_user_links(self):
        """Test if URL 'browse_follows' returns the correct user links for users user_3 is following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_3.id, 'follow': 'following'}))
        following = [uf.user for uf in UserFollower.objects.filter(follower=self.user_3)]
        for follower in following:
            url = reverse('profile', kwargs={'user_id': follower.id})
            self.assertContains(response, f'<a href="{url}">')

    def test_browse_following_not_contains_not_following_user_links(self):
        """Test if URL 'browse_follows' returns only the correct user links for users user_3 is following"""
        response = self.client.get(reverse('browse_follows',
                                           kwargs={'user_id': self.user_3.id, 'follow': 'following'}))
        # using set instead of list to get rid of duplicates
        all_users = set(User.objects.all())
        following = {uf.user for uf in UserFollower.objects.filter(follower=self.user_3)}
        not_following = all_users.difference(following)

        if self.user_3 in not_following:
            # self.user_3 must be removed if present because the view rightly contains a link to their profile
            not_following.remove(self.user_3)

        for user in not_following:
            url = reverse('profile', kwargs={'user_id': user.id})
            self.assertNotContains(response, f'<a href="{url}">')


class AddRemoveFollowersTests(TestCase):
    """Class for testing the adding and removal of followers"""

    def setUp(self):
        """Create test users and set up who is following whom for testing"""
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='user_1', avatar=self.file)
        self.user_1.set_password('bartestpass')
        self.user_1.save()
        self.user_2 = User.objects.create(username='user_2', avatar=self.file)
        self.user_2.set_password('bartestpass')
        self.user_2.save()

        UserFollower.objects.create(user=self.user_1, follower=self.user_2)

    def test_add_followee_through_api(self):
        """Test adding a followee directly through the API"""
        self.assertTrue(self.client.login(username='user_1', password='bartestpass'))
        followee_id = self.user_2.id
        response = self.client.put(path=f'/ajax/follow/{followee_id}')
        self.assertTrue(response.json()['success'])
        self.assertTrue(UserFollower.objects.get(user=self.user_2, follower=self.user_1))

    def test_add_followee_through_view(self):
        """Test adding a followee through reversing the URL"""
        self.assertTrue(self.client.login(username='user_1', password='bartestpass'))
        followee_id = self.user_2.id
        url = reverse('follow', kwargs={'followee_id': followee_id})
        response = self.client.put(path=url)
        self.assertTrue(response.json()['success'])
        self.assertTrue(UserFollower.objects.get(user=self.user_2, follower=self.user_1))

    def test_fail_to_add_followee_already_following(self):
        """Test adding a followee that is already being followed"""
        self.assertTrue(self.client.login(username='user_2', password='bartestpass'))
        followee_id = self.user_1.id
        url = reverse('follow', kwargs={'followee_id': followee_id})
        response = self.client.put(path=url)
        self.assertFalse(response.json()['success'])
        self.assertEqual(response.json()['error'], f'You are already following user {self.user_1.username}!')

    def test_remove_followee_through_api(self):
        """Test removing a followee directly through the API"""
        self.assertTrue(self.client.login(username='user_2', password='bartestpass'))
        followee_id = self.user_1.id
        response = self.client.put(path=f'/ajax/unfollow/{followee_id}')
        self.assertTrue(response.json()['success'])
        self.assertRaises(UserFollower.DoesNotExist, UserFollower.objects.get, user=self.user_1, follower=self.user_2)

    def test_remove_followee_through_view(self):
        """Test removing a followee through reversing the URL"""
        logged_in = self.client.login(username='user_2', password='bartestpass')
        self.assertTrue(logged_in)
        followee_id = self.user_1.id
        url = reverse('unfollow', kwargs={'followee_id': followee_id})
        response = self.client.put(path=url)
        self.assertTrue(response.json()['success'])
        self.assertRaises(UserFollower.DoesNotExist, UserFollower.objects.get, user=self.user_1, follower=self.user_2)

    def test_fail_to_remove_followee_not_following(self):
        """Test removing a followee that is not even being followed"""
        self.assertTrue(self.client.login(username='user_1', password='bartestpass'))
        followee_id = self.user_2.id
        url = reverse('unfollow', kwargs={'followee_id': followee_id})
        response = self.client.put(path=url)
        self.assertFalse(response.json()['success'])
        self.assertEqual(response.json()['error'], f'You are not following user {self.user_2.username}!')


class UserProfileTests(TestCase):
    """Class for testing the user profile"""

    def setUp(self):
        """Set up data for user profile view tests"""
        self.file = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user_1 = User.objects.create(username='test_user', avatar=self.file, bio='test_bio')
        self.user_1.set_password('test_password')
        self.user_1.save()

        self.user_2 = User.objects.create(username='test_user_2', avatar=self.file, bio='test_bio')
        self.user_2.set_password('test_password')
        self.user_2.save()

        self.post = Post.objects.create(
            description='test description shorter than 300 characters',
            author=self.user_1,
            image=self.file)

    def test_profile_status_code(self):
        """'browse_follows' page gives HTTP status code 200 for users user_1 is following"""
        response = self.client.get(f'/users/{self.user_1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_by_name(self):
        """'browse_follows' page for users user_1 is following via the URL name gives HTTP status code 200"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertEqual(response.status_code, 200)

    def test_profile_correct_template(self):
        """Test if URL 'browse_follows' uses browse_users.html for users user_1 is following"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertTemplateUsed(response, join(APP_NAME, 'profile.html'))

    def test_profile_contains_correct_html(self):
        """Test if URL 'browse_follows' returns HTML with 'Browse user_1's following"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertContains(response, f"<h2>{self.user_1.username}</h2>")

    def test_profile_has_post(self):
        """Test if user_1's profile view contains a post from user_1"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_1.id}))
        self.assertContains(response, self.post.description)

    def test_profile_has_no_other_posts(self):
        """Test if user_2's profile view does not contain a post from user_1"""
        response = self.client.get(reverse('profile',
                                           kwargs={'user_id': self.user_2.id}))
        self.assertNotContains(response, self.post.description)


class RegistrationViewTests(TestCase):
    """Tests for register view"""

    def setUp(self):
        """Registration view test setup"""
        self.file = File(open('static/dreamy/images/totally_not_a_default_avatar.png', 'rb'))
        self.default_avatar = File(open('static/dreamy/images/default_avatar.png', 'rb'))
        self.user = User.objects.create(username='test_user',
                                        bio='test bio shorter than 500 characters',
                                        avatar=self.file,
                                        password='test password')

        self.new_user_data = {'username': 'new_user',
                              'password1': self.user.password,
                              'password2': self.user.password,
                              'bio': self.user.bio,
                              'avatar': self.user.avatar}

    def test_register_correct_template(self):
        """Test if the correct registration template is used."""
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, join(APP_NAME, 'register.html'))

    def test_correct_avatar_set(self):
        """Test if the correct avatar is saved if given in the form"""
        self.client.post(reverse('register'), data=self.new_user_data)
        user = User.objects.get(username=self.new_user_data['username'])
        self.assertEqual(basename(user.avatar.url), basename(self.new_user_data['avatar'].name))

    def test_default_avatar_set(self):
        """Test if default avatar is set if an avatar is not specified"""
        self.new_user_data.pop('avatar')
        self.client.post(reverse('register'), data=self.new_user_data)
        user = User.objects.get(username=self.new_user_data['username'])
        avatar_regex = r'default_avatar.*\.png$'
        self.assertTrue(re.match(avatar_regex, basename(user.avatar.name)))

    def test_valid_data_correct_redirect_302(self):
        """Test if valid data passes, and also redirects to home/"""
        response = self.client.post(reverse('register'), data=self.new_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('home'))
