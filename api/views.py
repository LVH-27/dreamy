from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from dreamy.models import Post, UserFollower
import api.serializers as serializers
from api.permissions import IsAuthor, IsFollower


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing and detailing users"""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CreateUserView(generics.CreateAPIView):
    """This class defines the view for registering users"""

    model = User
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing posts"""

    permission_classes = [IsAuthor]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    @action(detail=False)
    def list_private(self, request, *args, **kwargs):
        """Fetch posts from followed users and serialize them"""
        posts = []
        followees = [uf.user for uf in UserFollower.objects.filter(follower=self.request.user)]
        [posts.extend(Post.objects.filter(author=user)) for user in followees]
        posts.sort(key=lambda post: post.date)
        return Response(serializers.PostSerializer(posts, many=True, context={'request': request}).data)


class UserFollowerViewSet(viewsets.ModelViewSet):
    """This class defines a view for listing UserFollowers"""

    permission_classes = [IsAuthenticated, IsFollower]
    queryset = UserFollower.objects.all()
    serializer_class = serializers.UserFollowerSerializer

    @action(detail=False)
    def following(self, request, *args, **kwargs):
        """Fetch all followees"""
        uf_followees = UserFollower.objects.filter(follower=self.request.user)
        return Response(serializers.UserFollowerSerializer(
                        uf_followees,
                        many=True,
                        context={'request': request}
                        ).data
                        )

    @action(detail=False)
    def followers(self, request, *args, **kwargs):
        """Fetch all followees"""
        uf_followers = UserFollower.objects.filter(user=self.request.user)
        return Response(serializers.UserFollowerSerializer(
                        uf_followers,
                        many=True,
                        context={'request': request}
                        ).data
                        )


@api_view(['POST'])
def register(request):
    serialized = serializers.UserSerializer(data=request.DATA)
    if serialized.is_valid():
        User.objects.create_user(
            serialized.init_data['username'],
            serialized.init_data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
