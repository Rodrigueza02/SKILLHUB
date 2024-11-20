from django.urls import path
from .views import home_view, register, login_view, messages_view

urlpatterns = [
    path('register/', register, name='register'),  
    path('login/', login_view, name='login'),
    path('messages/', messages_view, name='messages'),
    path('home/', home_view, name='home'),
]