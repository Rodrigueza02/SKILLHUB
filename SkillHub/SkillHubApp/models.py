from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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