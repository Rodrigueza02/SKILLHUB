from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

def validate_file_size(value):
    """
    Validador de tamaño de archivo
    Límite máximo: 50MB
    """
    max_size = 50 * 1024 * 1024  # 50 MB
    if value.size > max_size:
        raise ValidationError(f"El archivo no debe superar los {max_size / (1024 * 1024):.0f} MB")

class Profile(models.Model):
    """
    Perfil de usuario extendido
    """
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
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_account_type_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea un perfil automáticamente al crear un usuario
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Guarda el perfil del usuario
    """
    instance.profile.save()

class Skill(models.Model):
    """
    Habilidades de los usuarios
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Modelo de publicaciones con soporte multimedia
    """
    MEDIA_TYPES = [
        ('article', 'Artículo'),
        ('image', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Documento')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = RichTextField(max_length=800)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    media_type = models.CharField(
        max_length=20, 
        choices=MEDIA_TYPES, 
        default='article'
    )
    media_file = models.FileField(
        upload_to='post_media/', 
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    # Imágenes
                    'jpg', 'jpeg', 'png', 'gif', 'webp',
                    # Videos
                    'mp4', 'avi', 'mov', 'mkv', 'webm',
                    # Audio
                    'mp3', 'wav', 'ogg', 'm4a',
                    # Documentos
                    'pdf', 'doc', 'docx', 'txt', 'rtf'
                ]
            ),
            validate_file_size
        ],
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"{self.user.username}: {self.title or self.content[:50]}..."

class Message(models.Model):
    """
    Sistema de mensajería entre usuarios
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.sender} a {self.recipient} - {self.timestamp}"

class Connection(models.Model):
    """
    Modelo para gestionar conexiones entre usuarios
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado')
    ]

    from_user = models.ForeignKey(User, related_name='connections_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='connections_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"

    class Meta:
        unique_together = ('from_user', 'to_user')