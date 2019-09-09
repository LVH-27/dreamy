from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from os.path import join

from .forms import DreamyUserCreationForm
from . import PRETTY_APP_NAME, APP_NAME, models

# Create your views here.


def home(request):
    return render(request,
                  join(APP_NAME, 'index.html'),
                  {'PRETTY_APP_NAME': PRETTY_APP_NAME})


def register(request):
    if request.method == 'POST':
        form = DreamyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = DreamyUserCreationForm()
    return render(request,
                  join(APP_NAME, 'register.html'),
                  {'form': form, 'PRETTY_APP_NAME': PRETTY_APP_NAME})


def profile(request, user_id=None):
    if user_id is None:
        user_id = request.user.id
    user = get_user_model().objects.get(id=user_id)
    user_posts = models.Post.objects.filter(author=user)

    return render(request,
                  join(APP_NAME, 'profile.html'),
                  {'user': user,
                   'PRETTY_APP_NAME': PRETTY_APP_NAME,
                   'user_posts': user_posts})


def browse_users(request, user_id=None, follow=None):
    if follow is None:
        user_list = models.User.objects.all()
    else:
        # note: if follow is not None, the user_id cannot be None
        user = models.User.objects.get(id=user_id)
        if follow == 'followers':
            user_follower_list = models.UserFollower.objects.filter(user=user)
            user_list = [user_follower.follower for user_follower in user_follower_list]
        elif follow == 'following':
            user_follower_list = models.UserFollower.objects.filter(follower=user)
            user_list = [user_follower.user for user_follower in user_follower_list]

    paginator = Paginator(user_list, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request,
                  join(APP_NAME, 'browse_users.html'),
                  {'users': users,
                   'PRETTY_APP_NAME': PRETTY_APP_NAME})


def post(request, post_id):
    return f"Post: {post_id}"
