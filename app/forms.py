# en tu archivo forms.py
from django import forms
from .models import Casa

class CasaForm(forms.ModelForm):

    titulo = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Titulo'})
    )
    descripcion = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'placeholder': 'Descripcion'})
    )
    localidad = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Localidad'})
    )
    direccion = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Direccion'})
    )
    class Meta:
        model = Casa
        exclude = ['arrendador', 'imagen']
        fields = ['arrendador', 'titulo', 'descripcion', 'imagen', 'localidad', 'direccion']

class ImageUploadForm(forms.Form):
    imagen = forms.ImageField()
