from django import forms
from .models import Reclamacion

class ReclamacionForm(forms.ModelForm):
    class Meta:
        model = Reclamacion
        fields = ['titulo', 'descripcion']

    def __init__(self, *args, **kwargs):
        super(ReclamacionForm, self).__init__(*args, **kwargs)
        # Puedes personalizar el aspecto del formulario aquí si es necesario
