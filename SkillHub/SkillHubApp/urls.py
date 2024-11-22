from django.urls import path
from .views import (

    register,
    login_view,
    messages_view,
    home_professional_view,
    home_company_view,
    notifications_view,
    connections_view,
    profile_professional_view,
    edit_profile_professional,
    add_skill,
    send_message_view,
    create_post_view,
    logout_view,
    
)

urlpatterns = [

    path('register/', register, name='register'),  
    path('login/', login_view, name='login'),
    
    path('messages/', messages_view, name='messages'),
    path('notifications/', notifications_view, name='notifications'),
    path('connections/', connections_view, name='connections'),
    path('send-message/', send_message_view, name='send_message'),
    path('create-post/', create_post_view, name='create_post'),

    #professional
    path('home-professional/', home_professional_view, name='home-professional'),
    path('profile-professional/', profile_professional_view, name='profile-professional'),
    path('profile/edit-professional/', edit_profile_professional, name='edit-profile-professional'),
    path('profile/add_skill/',add_skill, name='add_skill'),

    #company
    path('home-company/', home_company_view, name= 'home-company'),
    
    path('logout/', logout_view, name='logout'),

]