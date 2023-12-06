from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import date

class InfoPagoClienteForm(forms.Form):
    template_name = 'info_pago_form_template.html'
    
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
    template_name = 'info_pago_form_template.html'
    
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

    
class InfoPagoTarjetaForm(forms.Form):
    template_name = 'info_pago_form_template.html'
    
    def validar_iban(valor: str):
        if valor.startswith('ES') and valor.isalnum() and len(valor) == 24:
            return valor
        else:
            raise ValidationError('IBAN inválido.')
        
    def validar_caducidad(valor: date):
        if valor > date.today():
            return valor
        else:
            raise ValidationError('Fecha de caducidad debe ser posterior al día de hoy.')
    
    def validar_cvv(valor: str):
        if valor.isnumeric():
            return valor
        else:
            raise ValidationError('CVV inválido.')
    
    iban = forms.CharField(
    max_length=24,
    widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'IBAN'
    }),
    validators=[validar_iban]
    )
    caducidad = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Caducidad (DD/MM/YYYY)'
        }),
        validators=[validar_caducidad]
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'CVV'
        }),
        validators=[validar_cvv]
    )
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
