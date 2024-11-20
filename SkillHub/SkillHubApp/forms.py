from django import forms
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    recipient_username = forms.CharField(label='Destinatario', max_length=150)

    class Meta:
        model = Message
        fields = ['recipient_username', 'content']

    def clean_recipient_username(self):
        username = self.cleaned_data.get('recipient_username')
        try:
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("El usuario no existe.")
        return recipient