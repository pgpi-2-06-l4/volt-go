from django import forms
from .models import Producto, MARCAS_CHOICES

class BusquedaForm(forms.Form):
    nombre = forms.CharField(required=False)
    empresa = forms.ChoiceField(required=False, choices=MARCAS_CHOICES, label='Empresa')
    precio_maximo = forms.FloatField(required=False, min_value=0, label='Precio Máximo')
