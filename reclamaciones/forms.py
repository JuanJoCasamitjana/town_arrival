from django import forms
from app.models import Casa

from reclamaciones.models import Reclamacion

class ReclamacionForm(forms.ModelForm):
    class Meta:
        model = Reclamacion
        fields = ['motivo', 'pretensiones', 'informacion_adicional']  

    def __init__(self, user, *args, **kwargs):
        super(ReclamacionForm, self).__init__(*args, **kwargs)
        # Filtrar las opciones del campo 'casa' basándonos en las casas del usuario
        self.fields['casa'].queryset = Casa.objects.filter(usuario=user)
