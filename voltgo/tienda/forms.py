from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import date

class InfoPagoClienteForm(forms.Form):
    template_name = 'info_pago_form.html'
    
    def validar_telefono(valor: str):
        if valor.isdigit():
            return valor
        else:
            raise ValidationError('Email inválido.')
        
    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Nombre'
        })
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Email'
        }),
        validators=[validate_email]
    )
    telefono = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Teléfono'
        }),
        validators=[validar_telefono]
    )
    
class InfoPagoDireccionForm(forms.Form):
    template_name = 'info_pago_form.html'
    
    def validar_cp(valor: str):
        if valor.isdigit():
            return valor
        else:
            raise ValidationError('Código postal inválido.')
    
    calle = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Calle'
        })
    )
    apartamento = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Apartamento'
        })
    )
    pais = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'País'
        })
    )
    ciudad = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Ciudad'
        })
    )
    codigo_postal = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Código postal'
        }),
        validators=[validar_cp]
    )

    
class InfoTipoPagoForm(forms.Form):
    template_name = 'info_pago_form.html'
    
    tipo_pago = forms.ChoiceField(
        choices=[
            (0, 'Contrareembolso'),
            (1, 'Pasarela de pago')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control mb-3',
            'selected':'Pasarela de pago'
        })
    )

from .models import Reclamacion

class ReclamacionForm(forms.ModelForm):
    class Meta:
        model = Reclamacion
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
        }
        required = {
            'titulo': True,
            'descripcion': True,
        }
        error_messages = {
            'titulo': {
                'required': 'El título es obligatorio.',
            },
            'descripcion': {
                'required': 'La descripción es obligatoria.',
            },
        }
