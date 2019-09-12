from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.contrib.auth import get_user_model

from dreamy.models import Post, UserFollower
import api.serializers as serializers


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing and detailing users"""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing posts"""

    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        """Save a Post instance"""
        serializer.save(author=self.request.user)


class UserFollowerViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing UserFollowers"""

    queryset = UserFollower.objects.all()
    serializer_class = serializers.UserFollowerSerializer


# @api_view(['POST'])
# def create_user(request):
#     return Response({
#         'users': reverse('users', request=request),
#         'posts': reverse('posts', request=request),
#         'user_followers': reverse('user_followers', request=request)
#     })
