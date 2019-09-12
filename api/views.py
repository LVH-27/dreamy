from rest_framework.response import Response
from rest_framework.decorators import api_view, action
# from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.views.defaults import bad_request

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

    @action(detail=False)
    def list_private(self, request, *args, **kwargs):
        posts = []
        followees = [uf.user for uf in UserFollower.objects.filter(follower=self.request.user)]
        [posts.extend(Post.objects.filter(author=user)) for user in followees]
        posts.sort(key=lambda post: post.date)
        return Response(serializers.PostSerializer(posts, many=True, context={'request': request}).data)


class UserFollowerViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing UserFollowers"""

    queryset = UserFollower.objects.all()
    serializer_class = serializers.UserFollowerSerializer

    def perform_create(self, serializer):
        """Save a UserFollower instance by setting the logged-in user as follower"""
        if UserFollower.objects.get(user=serializer.data['user'], follower=self.request.user):
            content = {'error': f'Already following {serializer.data["user"]}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return serializer.save(follower=self.request.user)


# @api_view(['POST'])
# def create_user(request):
#     return Response({
#         'users': reverse('users', request=request),
#         'posts': reverse('posts', request=request),
#         'user_followers': reverse('user_followers', request=request)
#     })
