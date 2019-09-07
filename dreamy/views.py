from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import PRETTY_APP_NAME

from os.path import join
# Create your views here.

APP_NAME = 'dreamy'


mock_posts = [
    {'id': 1,
     'author': 'rincewind',
     'date': '21.02.2014.',
     'description': 'This is test photo',
     'image': join('images', 'rincewind.png')
     },
    {'id': 2,
     'author': 'rincewind',
     'date': '21.03.2014.',
     'description': 'This is another test photo',
     'image': join('images', 'rincewind2.png')
     },
    {'id': 3,
     'author': 'rincewind',
     'date': '21.04.2014.',
     'description': 'This is yet another test photo',
     'image': join('images', 'rincewind3.png')
     },
    {'id': 4,
     'author': 'roncewind',
     'date': '21.04.2014.',
     'description': 'This is not mine',
     'image': join('images', 'roncewind.png')
     },
]


def home(request):
    return render(request,
                  join(APP_NAME, 'index.html'),
                  {'PRETTY_APP_NAME': PRETTY_APP_NAME})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,
                  join(APP_NAME, 'register.html'),
                  {'form': form, 'PRETTY_APP_NAME': PRETTY_APP_NAME})


def profile(request, user_id):
    user_posts = []
    for post in mock_posts:
        if post['author'] == 'rincewind':
            user_posts.append(post)
    return render(request,
                  join(APP_NAME, 'profile.html'),
                  {'user_id': user_id,
                   'PRETTY_APP_NAME': PRETTY_APP_NAME,
                   'user_posts': user_posts})


def post(request, post_id):
    return "Post: {post_id}".format(post_id=post_id)
