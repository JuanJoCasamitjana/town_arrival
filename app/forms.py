# en tu archivo forms.py
from django import forms
from .models import Casa, Comentario, Reclamacion

class CasaForm(forms.ModelForm):

    titulo = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Titulo',
            'class':'form-control'
            })
    )
    descripcion = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Descripcion',
            'class':'form-control'
            })
    )
    localidad = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Localidad',
            'class':'form-control'
            })
    )
    direccion = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Direccion',
            'class':'form-control'
            })
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
            'texto': forms.Textarea(attrs={
                'rows': 4,
                'class':'form-control'
                }),
        }

        

class ReclamacionForm(forms.ModelForm):
    class Meta:
        model = Reclamacion
        fields = ['texto', 'pretensiones']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4}),
            'pretensiones': forms.Textarea(attrs={'rows': 4}),
        }

tipos =("LB", "Dejar las llaves en buzon"),("LV", "Dejar las llaves con vecino"), ("LP", "Entrega de llaves personal")

class AlquilerForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha de inicio:',
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'type': 'date',
                'class':'form-control'
                }
            )
        )
    fecha_fin = forms.DateField(
        label='Fecha de fin:',
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'type': 'date',
                'class':'form-control'
                }
            )
        )
    modoEntrega = forms.ChoiceField(choices = tipos)

