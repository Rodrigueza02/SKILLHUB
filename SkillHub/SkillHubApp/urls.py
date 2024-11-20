from django.urls import path
from .views import register, login_view, home_view

urlpatterns = [
    path('register/', register, name='register'),  
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),      
]