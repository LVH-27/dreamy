from django.urls import include, path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'user_followers', views.UserFollowerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.CreateUserView.as_view(), name='register')
]
