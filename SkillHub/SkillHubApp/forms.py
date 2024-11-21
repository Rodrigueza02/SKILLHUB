from django import forms
from .models import Message, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

class MessageForm(forms.ModelForm):
    recipient_username = forms.CharField(label='Destinatario', max_length=150)

    class Meta:
        model = Message
        fields = ['content']  # Eliminamos recipient_username de aquí

    def clean_recipient_username(self):
        username = self.cleaned_data.get('recipient_username')
        try:
            recipient = User.objects.get(username=username)
            return recipient
        except User.DoesNotExist:
            raise forms.ValidationError("El usuario no existe.")
        
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
        # Validar que el correo electrónico sea único
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def clean_password2(self):
        # Validar que las contraseñas coincidan
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        
        return password2

    def save(self, commit=True):
        # Guardar usuario y tipo de cuenta
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        
        return user
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media_type', 'media_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Título del artículo',
                'class': 'form-control'
            }),
            'content': CKEditorWidget(config_name='default'),
            'media_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'media_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*,audio/*,application/pdf,application/msword'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        media_file = cleaned_data.get('media_file')
        media_type = cleaned_data.get('media_type')

        # Validaciones
        if not content and not media_file:
            raise forms.ValidationError("Debe proporcionar contenido de texto o un archivo multimedia.")

        # Validar longitud del contenido
        if content and len(content) > 800:
            raise forms.ValidationError("El contenido no debe superar los 800 caracteres.")

        return cleaned_data
    
    class Meta:
        model = Post
        fields = ['content', 'media_type', 'media_file']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Escribe tu publicación aquí...',
                'class': 'form-control'
            }),
            'media_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*,audio/*,application/pdf,application/msword'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        media_file = cleaned_data.get('media_file')
        media_type = cleaned_data.get('media_type')

        # Validar que al menos un campo tenga contenido
        if not content and not media_file:
            raise forms.ValidationError("Debe proporcionar contenido de texto o un archivo multimedia.")

        # Validar que si se selecciona un tipo de medio, se adjunte un archivo
        if media_type and not media_file:
            raise forms.ValidationError("Debe adjuntar un archivo si selecciona un tipo de medio.")

        return cleaned_data