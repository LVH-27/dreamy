from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from datetime import datetime

from os.path import join

from .forms import DreamyUserCreationForm, DreamySubmitPostForm
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
        user_category = 'users'
        user_list = models.User.objects.all().order_by('username')
    else:
        # note: if follow is not None, the user_id cannot be None
        user = models.User.objects.get(id=user_id)
        if follow == 'followers':
            user_category = f'{user.username}\'s followers'
            user_follower_list = models.UserFollower.objects.filter(user=user)
            user_list = [user_follower.follower for user_follower in user_follower_list]
        elif follow == 'following':
            user_category = f'users {user.username} follows'
            user_follower_list = models.UserFollower.objects.filter(follower=user)
            user_list = [user_follower.user for user_follower in user_follower_list]
        user_list.sort(key=lambda x: x.username)

    if request.user.is_authenticated:
        current_user_following_list = [user_follower.user for user_follower in
                                       models.UserFollower.objects.filter(follower=request.user)]
    else:
        current_user_following_list = []
    user_following_pairs = []
    for user in user_list:
        user_following_pairs.append((user, user in current_user_following_list))

    paginator = Paginator(user_following_pairs, 20)
    page = request.GET.get('page')
    users_following = paginator.get_page(page)
    return render(request,
                  join(APP_NAME, 'browse_users.html'),
                  {'users_following': users_following,
                   'PRETTY_APP_NAME': PRETTY_APP_NAME,
                   'user_category': user_category})


def submit(request):
    if request.method == 'POST':
        form = DreamySubmitPostForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            author = form.cleaned_data['author']
            date = form.cleaned_data['date']
            post = models.Post.objects.create(
                description=description,
                image=image,
                author=author,
                date=date
            )
            post.save()
            return redirect(f'/post/{post.id}/')
    else:
        form = DreamySubmitPostForm(initial={'author': request.user, 'date': datetime.now()})
    return render(request,
                  join(APP_NAME, 'submit.html'),
                  {'form': form,
                   'PRETTY_APP_NAME': PRETTY_APP_NAME})


def timeline(request, private):
    if private:
        title = "Private timeline"
        target_users = [uf.user for uf in models.UserFollower.objects.filter(follower=request.user)]
    else:
        title = "Public timeline"
        target_users = list(models.User.objects.all())

    posts = []
    [posts.extend(models.Post.objects.filter(author=user)) for user in target_users]
    posts.sort(key=lambda post: post.date)

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request,
                  join(APP_NAME, 'timeline.html'),
                  {'posts': posts,
                   'PRETTY_APP_NAME': PRETTY_APP_NAME,
                   'title': title})


def view_post(request, post_id):
    post = models.Post.objects.get(id=post_id)
    return render(request, 'dreamy/post.html', {'post': post})


def follow(request, followee_id):
    followee = models.User.objects.get(id=followee_id)
    try:
        uf = models.UserFollower(user=followee, follower=request.user)
        uf.save()
    except IntegrityError:
        return JsonResponse({'success': False,
                             'error': f'You are already following user {followee.username}!'})
    except ValueError:
        return JsonResponse({'success': False,
                             'error': 'You must be logged in to follow users!'})
    return JsonResponse({'success': True})


def unfollow(request, followee_id):
    followee = models.User.objects.get(id=followee_id)
    print(followee)
    try:
        uf = models.UserFollower.objects.get(user=followee, follower=request.user)
        uf.delete()
    except models.UserFollower.DoesNotExist:
        return JsonResponse({'success': False,
                             'error': f'You are not following user {followee.username}!'})
    except ValueError:
        return JsonResponse({'success': False,
                             'error': 'You must be logged in to unfollow users!'})
    return JsonResponse({'success': True})
