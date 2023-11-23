from django import forms

class BusquedaForm(forms.Form):
    autonomia = forms.IntegerField(required=False, min_value=0, label='Autonomía (horas)')
    velocidad_maxima = forms.IntegerField(required=False, min_value=0, label='Velocidad Máxima (Km/h)')
    precio_maximo = forms.FloatField(required=False, min_value=0, label='Precio Máximo')