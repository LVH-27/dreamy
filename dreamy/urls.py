"""dreamy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from dreamy import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('submit/', views.submit, name='submit'),
    path('post/<post_id>/', views.view_post, name='view_post'),
    path('timeline/', views.timeline, {'private': False}, name='public_timeline'),
    path('timeline/private', views.timeline, {'private': True}, name='private_timeline'),
    path('users/', views.browse_users, name='browse_users'),
    path('users/<user_id>/', views.profile, name='profile'),
    re_path(r'users/(?P<user_id>[0-9]+)/(?P<follow>(followers|following))/', views.browse_users, name='browse_follows'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('ajax/follow/<followee_id>', views.follow, name='follow'),
    path('ajax/unfollow/<followee_id>', views.unfollow, name='unfollow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
