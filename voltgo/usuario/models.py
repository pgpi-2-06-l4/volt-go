from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime

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

class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    direction = models.CharField(blank=True, max_length=100)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return 'Profile for user {self.user.username}'


def validar_fecha(fecha):
    fecha_limite = datetime.now().date()
    if fecha > fecha_limite:
        raise ValidationError(_('La fecha no puede ser superior a la fecha actual.'),
                              params={'fecha_limite': fecha_limite})
    if fecha == fecha_limite:
        raise ValidationError(_('La fecha no puede ser igual a la fecha actual.'),
                              params={'fecha_limite': fecha_limite})
    

def validate_letters(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError('La cadena solo puede contener letras')
    
class Perfil(models.Model):
    
    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"
            
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(validators=[validar_fecha], blank=True, null=True)
    
    telefono_validator = RegexValidator(
        regex=r'^(\+34|0034|34)?[6789]\d{8}$',
        message="Formato invalido."
    )
    
    telefono = models.CharField(max_length=9, validators=[telefono_validator], blank=True, null=True)

    def __str__(self):
        return self.usuario.username
    
class Direccion(models.Model):

    class Meta:
        verbose_name = "direccion"
        verbose_name_plural = "direcciones"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True, blank = True)
    calle = models.CharField(max_length=100, validators=[validate_letters])
    apartamento = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, choices=PAISES_CHOICES)
    ciudad = models.CharField(max_length=100, choices=CIUDADES_CHOICES)
    codigo_postal = models.CharField(max_length=5, validators=[RegexValidator(regex='^\d{5}$', message='El código postal debe contener 5 dígitos exactamente')])



    def __str__(self):
        return f"{self.calle}, {self.apartamento}, {self.ciudad} {self.pais}"
    




