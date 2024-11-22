from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,UserChangeForm 
from django.contrib.auth import login, authenticate, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Message, Skill, Post
from .forms import MessageForm, CustomRegisterForm, PostForm
from django.contrib import messages 

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión inmediatamente después de registrarse
            # Redirigir según el tipo de cuenta
            if form.cleaned_data['account_type'] == 'professional':
                return redirect('home-professional')  # Redirigir a home_professional
            elif form.cleaned_data['account_type'] == 'empresa':
                return redirect('home-company')  # Redirigir a home-company
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir según el tipo de cuenta
            if hasattr(user, 'profile'):
                if user.profile.account_type == 'professional':
                    return redirect('home-professional')  # Redirigir a home_professional
                elif user.profile.account_type == 'empresa':
                    return redirect('home-company')  # Redirigir a home-company
        else:
            error_message = "Nombre de usuario o contraseña incorrectos."
            return render(request, 'registration/login.html', {'error_message': error_message})
    return render(request, 'registration/login.html')

@login_required
def home_professional_view(request):
    # Obtener todas las publicaciones ordenadas por timestamp
    posts = Post.objects.all().order_by('-timestamp')
    
    # Configurar el formulario para crear publicaciones
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Publicación creada exitosamente')
            return redirect('home-professional')
    else:
        form = PostForm()

    return render(request, 'SkillHubApp/inicio/home_professional.html', {
        'user': request.user,
        'posts': posts,
        'form': form,
    })

@login_required
def home_company_view(request):
    # Obtener todas las publicaciones ordenadas por timestamp
    posts = Post.objects.all().order_by('-timestamp')
    
    # Configurar el formulario para crear publicaciones
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Publicación creada exitosamente')
            return redirect('home-company')
    else:
        form = PostForm()

    return render(request, 'SkillHubApp/inicio/home-company.html', {
        'user': request.user,
        'posts': posts,
        'form': form,
    })

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
    
    return render(request, 'SkillHubApp/mensajes/messages.html', {
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
    return render(request, 'SkillHubApp/notificaciones/notifications.html', {'notifications': notifications})

@login_required
def connections_view(request):
    connections = [
        {"username": "Usuario1", "status": "Conectado"},
        {"username": "Usuario2", "status": "Conectado"},
        {"username": "Usuario3", "status": "Pendiente"},
    ]
    return render(request, 'SkillHubApp/conexiones/connections.html', {'connections': connections})

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
def edit_profile_professional(request):
    if request.method == 'POST':
        # Lógica para manejar la edición del perfil
        # ...
        return redirect('profile-professional')  # Asegúrate de usar el nombre correcto aquí
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'SkillHubApp/perfiles/edit_profile_professional.html', {
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
def profile_professional_view(request):
    # Obtén las habilidades del usuario actual
    skills = Skill.objects.filter(user=request.user)
    return render(request, 'SkillHubApp/perfiles/profile_professional.html', {'skills': skills})

@login_required
def send_message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = form.cleaned_data['recipient_username']
            message.save()
            messages.success(request, 'Mensaje enviado exitosamente')
            return redirect('messages')
    else:
        form = MessageForm()
    
    return render(request, 'SkillHubApp/mensajes/send_message.html', {'form': form})

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Publicación creada exitosamente')

            # Redirigir según el tipo de cuenta
            if hasattr(request.user, 'profile'):
                if request.user.profile.account_type == 'professional':
                    return redirect('home-professional')  # Redirigir a home_professional
                elif request.user.profile.account_type == 'company':
                    return redirect('home-company')  # Redirigir a home-company
        else:
            messages.error(request, 'Por favor, revisa los errores en el formulario')
    else:
        form = PostForm()

    return render(request, 'SkillHubApp/inicio/create_post.html', {'form': form})

@login_required
def manage_applications_view(request):
    # Lógica para gestionar postulaciones
    return render(request, 'SkillHubApp/inicio/manage_applications.html')