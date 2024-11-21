from django.urls import path
from .views import (

    register,
    login_view,
    messages_view,
    home_view,
    notifications_view,
    connections_view,
    profile_view,
    edit_profile,
    add_skill,
    send_message_view,
    create_post_view,
    logout_view,
    
)

urlpatterns = [
    path('register/', register, name='register'),  
    path('login/', login_view, name='login'),
    path('messages/', messages_view, name='messages'),
    path('home/', home_view, name='home'),
    path('notifications/', notifications_view, name='notifications'),
    path('connections/', connections_view, name='connections'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/add_skill/',add_skill, name='add_skill'),
    path('send-message/', send_message_view, name='send_message'),
    path('create-post/', create_post_view, name='create_post'),
    path('logout/', logout_view, name='logout'),
]