# en tu archivo forms.py
from django import forms
from .models import Casa, Comentario

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

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4}),
        }

class AlquilerForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha de inicio:',
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={'type': 'date'}
            )
        )
    fecha_fin = forms.DateField(
        label='Fecha de fin:',
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={'type': 'date'}
            )
        )