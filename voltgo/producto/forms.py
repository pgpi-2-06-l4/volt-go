from django import forms
from .models import Producto

class BusquedaForm(forms.Form):
    nombre = forms.CharField(required=False)
    empresa = forms.CharField(required=False)
    precio_maximo = forms.FloatField(required=False, min_value=0, label='Precio Máximo')
