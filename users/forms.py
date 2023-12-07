from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico',
            'class':'form-control'
            }),
        label='',  # Eliminar el label
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de usuario',
            'class':'form-control'
            }),
        label='',  # Eliminar el label
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class':'form-control'
            }),
        help_text='',  # Eliminar la ayuda visual de requisitos de contraseña
        label='',  # Eliminar el label
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña',
            'class':'form-control'
            }),
        help_text='',  # Eliminar la ayuda visual de requisitos de contraseña
        label='',  # Eliminar el label
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Biografía',
            'class':'form-control'
            }),
        help_text='',
        label='', 
        )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'rol']
        exclude = ['avatar']

class UserLoginForm2(AuthenticationForm):
    class Meta:
        fields = ['email', 'password']
        
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class': 'form-control',
            }
        ),
        label='',
    )
    password = forms.CharField(widget=forms.PasswordInput(
            attrs={
            'placeholder': 'Contraseña',
            'class':'form-control'
            }),
            help_text='',
            label='', 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
            'placeholder': 'Email',
            'class':'form-control'
            }
        ),
        help_text='',
        label='', 
    )
    password = forms.CharField(widget=forms.PasswordInput(
            attrs={
            'placeholder': 'Contraseña',
            'class':'form-control'
            }),
            help_text='',
            label='', 
    )
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)

                if not check_password(password, user.password):
                    raise forms.ValidationError(
                        ("Las credenciales ingresadas no son válidas.")
                    )
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "El usuario con este correo electrónico no existe."
                )
        return self.cleaned_data

class ImageUploadForm(forms.Form):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class':'btn btn-secondary'
            }
    ))
