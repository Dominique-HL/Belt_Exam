from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.messages import get_messages
from django.contrib import messages
import re
from .models import User, Thought

# Create your views here.

def index(request):
    return render(request, "index.html")
    
def users(request, user_id):
    author = User.objects.get(id=user_id)
    context = {
        'thoughts': Thought.objects.filter(author = author),
        'author': author 
    }
    return render(request, "users.html", context)

def thoughts(request):
    registered_users = User.objects.all()
    current_user = User.objects.get(id = request.session['id']) 
    favourites = Thought.objects.filter(favouriting_users=current_user)
    allthoughts = Thought.objects.all().order_by('-id').exclude(id__in=[f.id for f in favourites])
    context = {
        "registered_users": registered_users,
        "current_user": current_user,
        "thoughts": allthoughts,
        "favourites" : favourites
    }

    return render(request, "thoughts.html", context)

def register(request):

    if request.method == "GET":
        return redirect ('/')
    new_user = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'])
    if new_user['status'] == True:
        request.session['id'] = new_user['created_user'].id
        return redirect('/thoughts')
    else:
        messages.error(request, new_user['errors'], extra_tags = "register")
        return redirect ('/')

def login(request):

    if request.method == "GET":
        return redirect ('/')
    current_user = User.objects.login_validate(request.POST['email'], request.POST['password'])
    if current_user['status'] == True:
        request.session['id'] = current_user['found_user'].id
        return redirect('/thoughts')
    else:
        messages.error(request, current_user['errors'], extra_tags = "login")
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')




def thought_post(request):
    if request.method == "GET":
        return redirect ('/')
    if request.method == "POST":
        thought_text = request.POST['thought']
        user_id = request.session['id']
        thoughted_by = request.POST['thought_author']

        result = Thought.objects.validate_thought(thought_text, user_id, thoughted_by)
        if result['status'] == True:
            messages.info(request, result['errors'])
            return redirect ('/thoughts')
        messages.error(request, result['errors'], extra_tags = "thought_post")
        return redirect('/thoughts')

def add_favorite_for_current_user(request, thought_id):
    user_id = request.session['id']
    Thought.objects.add_favourite_for_user(user_id, thought_id)
    return redirect('/thoughts')

def remove_from_favourites(request, thought_id):
    user_id = request.session['id']
    Thought.objects.remove_from_favorites(user_id, thought_id)
    return redirect('/thoughts')

def dashboard(request):
    return redirect('/thoughts')


