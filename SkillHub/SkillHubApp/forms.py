from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from .models import Message, Post, Skill

class CustomRegisterForm(UserCreationForm):
    ACCOUNT_TYPES = [
        ('professional', 'Profesional'),
        ('company', 'Empresa')
    ]

    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150,
        help_text='Requerido. 150 caracteres o menos.'
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=254,
        help_text='Introduzca una dirección de correo electrónico válida.'
    )
    
    account_type = forms.ChoiceField(
        label='Tipo de Cuenta',
        choices=ACCOUNT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Su contraseña debe contener al menos 8 caracteres.'
    )
    
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Introduzca la misma contraseña que antes, para verificación.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'account_type', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        
        return user

class MessageForm(forms.ModelForm):
    recipient_username = forms.CharField(label='Destinatario', max_length=150)

    class Meta:
        model = Message
        fields = ['content']

    def clean_recipient_username(self):
        username = self.cleaned_data.get('recipient_username')
        try:
            recipient = User.objects.get(username=username)
            return recipient
        except User.DoesNotExist:
            raise forms.ValidationError("El usuario no existe.")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Título del artículo',
                'class': 'form-control'
            }),
            'content': CKEditorWidget(config_name='default'),
            'media_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*,audio/*,application/pdf,application/msword'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        media_file = cleaned_data.get('media_file')

        # Validaciones
        if not content and not media_file:
            raise forms.ValidationError("Debe proporcionar contenido de texto o un archivo multimedia.")

        # Validar longitud del contenido
        if content and len(content) > 800:
            raise forms.ValidationError("El contenido no debe superar los 800 caracteres.")

        return cleaned_data

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre de la habilidad',
                'class': 'form-control'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("El nombre de la habilidad no puede estar vacío.")
        return name