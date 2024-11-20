from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,UserChangeForm 
from django.contrib.auth import login, authenticate, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Message, Skill
from .forms import MessageForm
from django.contrib import messages 

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
    return render(request, 'SkillHubApp/home.html', {'user': request.user})

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

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']
        # Elimina campos sensibles como password
        exclude = ('password',)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Separa la validación y guardado de los formularios
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        # Valida cada formulario por separado
        user_form_valid = user_form.is_valid()
        password_form_valid = password_form.is_valid()

        if user_form_valid:
            user_form.save()
            messages.success(request, 'Información de perfil actualizada.')

        if password_form_valid:
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada exitosamente.')

        # Redirige solo si al menos un formulario es válido
        if user_form_valid or password_form_valid:
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'SkillHubApp/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })

@login_required
def add_skill(request):
    if request.method == 'POST':
        name = request.POST.get('skill_name')
        # Lógica para crear una nueva habilidad
        Skill.objects.create(user=request.user, name=name)
        return redirect('profile')
    return redirect('profile')

@login_required
def profile_view(request):
    # Obtén las habilidades del usuario actual
    skills = Skill.objects.filter(user=request.user)
    return render(request, 'SkillHubApp/profile.html', {'skills': skills})

@login_required
def send_message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Mensaje enviado exitosamente')
            return redirect('messages')
    else:
        form = MessageForm()
    
    return render(request, 'SkillHubApp/send_message.html', {'form': form})