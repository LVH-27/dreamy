from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """Overridden abstract User class to add bio, birth date and avatar fields"""

    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


class Post(models.Model):
    """ORM model for a Dreamy post"""

    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='posts')
    date = models.DateField()

    def __repr__(self):
        """Custom string representation"""
        return f"<Post: {self.description[:50]}>"


class UserFollower(models.Model):
    """Link table which links a user and their followers"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='users')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='followers')

    def __repr__(self):
        """Custom string representation"""
        return f"<User {self.user} - Follower {self.follower}>"
