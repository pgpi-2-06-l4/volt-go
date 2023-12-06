from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class InfoPagoClienteForm(forms.Form):
    template_name = 'info_pago_form.html'
    
    def __init__(self, *args, **kwargs):
        if 'disabled' in kwargs:
            del kwargs['disabled']
            for field in self.declared_fields.values():
                field.disabled = 'disabled'
        super(InfoPagoClienteForm, self).__init__(*args, **kwargs)
            
    
    def validar_nombre(valor: str):
        if valor.isalpha():
            return valor
        else:
            raise ValidationError('Nombre inválido.')
    
    def validar_telefono(valor: str):
        if valor.isdigit():
            return valor
        else:
            raise ValidationError('Teléfono inválido.')
        
    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Nombre',
            'pattern': '[A-Za-z ]+',
            'type': 'text'
        }),
        validators=[validar_nombre]
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
            'placeholder': 'Teléfono',
            'pattern': '[0-9]+'
        }),
        validators=[validar_telefono]
    )

    
class InfoPagoDireccionForm(forms.Form):
    template_name = 'info_pago_form.html'
    
    def __init__(self, *args, **kwargs):
        if 'disabled' in kwargs:
            del kwargs['disabled']
            for field in self.declared_fields.values():
                field.disabled = 'disabled'
        super(InfoPagoDireccionForm, self).__init__(*args, **kwargs)
    
    PAISES_CHOICES = [
        ('ESP', 'ESP')
    ]

    CIUDADES_CHOICES = [
        ('Huelva', 'Huelva'),
        ('Sevilla', 'Sevilla'),
        ('Cordoba', 'Cordoba'),
        ('Jaen', 'Jaen'),
        ('Cadiz', 'Cadiz'),
        ('Malaga', 'Malaga'),
        ('Granada', 'Granada'),
        ('Almeria', 'Almeria'),
        ('Badajoz', 'Badajoz'),
        ('Ciudad Real', 'Ciudad Real'),
        ('Albacete', 'Albacete'),
        ('Murcia', 'Murcia'),
        ('Alicante', 'Alicante'),
        ('Caceres', 'Caceres'),
        ('Toledo', 'Toledo'),
        ('Cuenca', 'Cuenca'),
        ('Valencia', 'Valencia'),
        ('Salamanca', 'Salamanca'),
        ('Avila', 'Avila'),
        ('Madrid', 'Madrid'),
        ('Guadalajara', 'Guadalajara'),
        ('Teruel', 'Teruel'),
        ('Castellon', 'Castellon'),
        ('Zamora', 'Zamora'),
        ('Valladolid', 'Valladolid'),
        ('Segovia', 'Segovia'),
        ('Soria', 'Soria'),
        ('Zaragoza', 'Zaragoza'),
        ('Tarragona', 'Tarragona'),
        ('Pontevedra', 'Pontevedra'),
        ('Orense', 'Orense'),
        ('Leon', 'Leon'),
        ('Palencia', 'Palencia'),
        ('Burgos', 'Burgos'),
        ('La Rioja', 'La Rioja'),
        ('Navarra', 'Navarra'),
        ('Huesca', 'Huesca'),
        ('Lerida', 'Lerida'),
        ('Barcelona', 'Barcelona'),
        ('Gerona', 'Gerona'),
        ('Navarra', 'Navarra'),
        ('Vizacaya', 'Vizcaya'),
        ('Guipuzcoa', 'Guipuzcoa'),
        ('Alava', 'Alava'),
        ('Cantabria', 'Cantabria'),
        ('Asturias', 'Asturias'),
        ('Lugo', 'Lugo'),
        ('La Coruña', 'La Coruña')    
    ]
    
    def validar_calle(valor: str):
        if valor.isalpha():
            return valor
        else:
            raise ValidationError('Calle inválida.')
    
    def validar_cp(valor: str):
        if valor.isdigit():
            return valor
        else:
            raise ValidationError('Código postal inválido.')
    
    calle = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Calle',
            'pattern': '[A-Za-z ]+',
            'type': 'text'
        }),
        validators=[validar_calle]
    )
    apartamento = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Apartamento',
            'type': 'text'
        })
    )
    pais = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'País'
            }
        ),
        choices=PAISES_CHOICES
    )
    ciudad = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ciudad'
            }
        ),
        choices=CIUDADES_CHOICES
    )
    codigo_postal = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Código postal',
            'pattern': '[0-9]+',
            'type': 'number'
        }),
        validators=[validar_cp]
    )

    
class InfoTipoPagoForm(forms.Form):
    template_name = 'info_pago_form.html'
    
    def __init__(self, *args, **kwargs):
        if 'disabled' in kwargs:
            del kwargs['disabled']
            for field in self.declared_fields.values():
                field.disabled = 'disabled'
        super(InfoTipoPagoForm, self).__init__(*args, **kwargs)
    
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
