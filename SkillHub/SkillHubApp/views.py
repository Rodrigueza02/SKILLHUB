from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

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

@login_required  
def home_view(request):
    return render(request, 'SkillHubApp/home.html')

@login_required  
def messages_view(request):
    messages = [
        {"sender": "Usuario1", "content": "Hola, ¿cómo estás?"},
        {"sender": "Usuario2", "content": "¿Te gustaría conectar?"},
    ]
    return render(request, 'SkillHubApp/messages.html', {'messages': messages})

@login_required
def notifications_view(request):
    notifications = [
        {"content": "Usuario1 te ha enviado un mensaje."},
        {"content": "Usuario2 ha comentado en tu publicación."},
        {"content": "Usuario3 te ha seguido."},
    ]
    return render(request, 'SkillHubApp/notifications.html', {'notifications': notifications})

@login_required
def connections_view(request):
    connections = [
        {"username": "Usuario1", "status": "Conectado"},
        {"username": "Usuario2", "status": "Conectado"},
        {"username": "Usuario3", "status": "Pendiente"},
    ]
    return render(request, 'SkillHubApp/connections.html', {'connections': connections})

@login_required
def logout_view(request):
    logout(request) 
    return redirect('login')

