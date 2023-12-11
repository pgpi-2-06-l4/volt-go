from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


MARCAS_CHOICES = [
    ('', 'Todos los modelos'),
    ('Harley Davidson', 'Harley Davidson'),
    ('Ducati', 'Ducati'),
    ('Aprilia', 'Aprilia'),
    ('BMW', 'BMW'),
    ('Yamaha', 'Yamaha'),
    ('Honda', 'Honda'),
    ('Suzuki', 'Suzuki'),
    ('Kawasaki', 'Kawasaki'),
    ('KTM', 'KTM'),
    ('Triumph', 'Triumph'),
    ('Benelli', 'Benelli'),
    ('Montesa', 'Montesa'),
    ('Moto Guzzi', 'Moto Guzzi')
]


class Caracteristica(models.Model):
    class Meta:
        verbose_name = "caracteristica"
        verbose_name_plural = "caracteristicas"

    TIPOS = [
        ("AT", "Autonomía"),
        ("VM", "Velocidad máxima"),
        ("TC", "Tiempo de carga"),
        ("P", "Peso"),
    ]

    nombre = models.CharField(max_length=50, choices=TIPOS)
    valor = models.PositiveIntegerField(blank=False)

    def __str__(self) -> str:
        return self.nombre


class Producto(models.Model):
    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    nombre = models.CharField(max_length=50, null=False, unique=False)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    url_imagen = models.URLField(null=False)
    precio_base = models.FloatField(null=False, default=0.0, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(null=False, default=1)
    empresa = models.CharField(max_length=100, choices=MARCAS_CHOICES)

    caracteristicas = models.ManyToManyField(Caracteristica)

    def __str__(self) -> str:
        return self.nombre

class ItemCarrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
    
    def get_precio_total_producto(self):
        return self.producto.precio_base * self.cantidad
    
    def aumentar_cantidad(self, cantidad):  
        self.cantidad += cantidad
        self.save()

class Comentario(models.Model):
    class Meta:
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=500, blank=False)
    fecha_comentario = models.DateField(auto_now=True)
