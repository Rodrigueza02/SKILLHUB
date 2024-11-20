from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            error_message = "Nombre de usuario o contraseña incorrectos."
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')

def home_view(request):
    return render(request, 'SkillHubApp/home.html') 

def messages_view(request):
    messages = [
        {"sender": "Usuario1", "content": "Hola, ¿cómo estás?"},
        {"sender": "Usuario2", "content": "¿Te gustaría conectar?"},
    ]
    return render(request, 'SkillHubApp/messages.html', {'messages': messages})