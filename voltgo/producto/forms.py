from django import forms
from .models import MARCAS_CHOICES
from .models import Comentario

class BusquedaForm(forms.Form):
    nombre = forms.CharField(required=False)
    empresa = forms.ChoiceField(required=False, choices=MARCAS_CHOICES, label='Empresa')
    precio_maximo = forms.FloatField(required=False, min_value=0, label='Precio Máximo')

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']
