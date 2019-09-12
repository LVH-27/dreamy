from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from dreamy.models import UserFollower, Post

User = get_user_model()


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Post model serializer"""

    class Meta:
        """Mapping serializer to Post model"""

        model = Post
        view_name = 'post_detail'
        fields = ['url', 'image', 'description']


class UserFollowerSerializer(serializers.HyperlinkedModelSerializer):
    """UserFollower model serializer"""

    class Meta:
        """Mapping serializer to UserFollower model"""

        model = UserFollower
        view_name = 'followers'
        fields = ['url', 'user', 'follower']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User model serializer"""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        """Mapping serializer to User model"""

        model = User
        view_name = 'user_detail'
        fields = ['url', 'username', 'password']

    def create(self, validated_data):
        """Password hashing"""
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
