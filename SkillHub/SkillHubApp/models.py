from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import FileExtensionValidator, ValidationError


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient} at {self.timestamp}"

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ACCOUNT_TYPES = [
        ('professional', 'Profesional'),
        ('company', 'Empresa')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(
        max_length=20, 
        choices=ACCOUNT_TYPES, 
        default='professional'
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_account_type_display()}"

@receiver(post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)  # Limite de caracteres
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."  # Muestra los primeros 20 caracteres

def validate_file_size(value):
    filesize = value.size
    
    # Límite de 10MB para cada archivo
    if filesize > 50 * 1024 * 1024:
        raise ValidationError("El archivo no debe superar los 50MB")

class Post(models.Model):
    MEDIA_TYPES = [
        ('image', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Documento')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Campos multimedia
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, blank=True, null=True)
    media_file = models.FileField(
        upload_to='post_media/', 
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    # Imágenes
                    'jpg', 'jpeg', 'png', 'gif', 
                    # Videos
                    'mp4', 'avi', 'mov', 
                    # Audio
                    'mp3', 'wav', 'ogg',
                    # Documentos
                    'pdf', 'doc', 'docx', 'txt'
                ]
            ),
            validate_file_size
        ],
        blank=True, 
        null=True
    )

    def clean(self):
        # Validar que al menos un campo tenga contenido
        if not self.content and not self.media_file:
            raise ValidationError("Debe proporcionar contenido de texto o un archivo multimedia.")

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."