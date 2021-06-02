from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('thoughts', views.thoughts),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('thought', views.thought_post),
    path('thought/<int:thought_id>', views.add_favorite_for_current_user),
    path('remove/<int:thought_id>', views.remove_from_favourites),
    path('users/<int:user_id>', views.users),
    path('dashboard', views.dashboard)
]