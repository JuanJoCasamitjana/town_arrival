from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        label='',  # Eliminar el label
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        label='',  # Eliminar el label
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        help_text='',  # Eliminar la ayuda visual de requisitos de contraseña
        label='',  # Eliminar el label
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        help_text='',  # Eliminar la ayuda visual de requisitos de contraseña
        label='',  # Eliminar el label
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(label='',  # Eliminar el label
        widget=forms.Textarea(attrs={'placeholder': 'Biografía'})
        )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'rol']
        exclude = ['avatar']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ImageUploadForm(forms.Form):
    avatar = forms.ImageField()
