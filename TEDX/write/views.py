from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import Topic, User, Post, Comment
from .forms import  UserForm, PostForm, CommentForm, SearchForm

# Create your views here.




def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(body__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
   
    context = { 'topics': topics, 'posts': posts}
    
    return render(request, 'write/home.html', context)

