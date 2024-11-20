from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # Establece el remitente como el usuario actual
            message.recipient = form.cleaned_data['recipient_username']  # Obtiene el destinatario
            message.save()
            return redirect('messages')  # Redirige a la vista de mensajes después de enviar
    else:
        form = MessageForm()

    # Obtener mensajes recibidos por el usuario actual
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    
    return render(request, 'SkillHubApp/messages.html', {
        'form': form,
        'received_messages': received_messages,
    })


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

