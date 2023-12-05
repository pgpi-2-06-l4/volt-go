from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from producto.models import Producto

class Venta(models.Model):
    class Meta():
        verbose_name = "venta"
        verbose_name_plural = "ventas"

    class EstadoVenta(models.IntegerChoices):
        POR_PAGAR = 0, ('Por pagar')
        PAGADO = 1, ('Pagado')
        
    class EstadoEnvio(models.IntegerChoices):
        EN_ALMACEN = 0, ('En almacen')
        EN_REPARTO = 1, ('En reparto')
        ENTREGADO = 2, ('Entregado')

    class TipoPago(models.IntegerChoices):
        CONTRAREEMBOLSO = 0, ('Contrareembolso')
        PASARELA = 1, ('Pasarela')
     
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=True)
    estado_venta = models.IntegerField(
        default=EstadoVenta.POR_PAGAR,
        choices=EstadoVenta.choices
    )   
    estado_envio = models.IntegerField(
        default=EstadoEnvio.EN_ALMACEN,
        choices=EstadoEnvio.choices
    )
    tipo_pago = models.IntegerField(
        default=TipoPago.PASARELA,
        choices=TipoPago.choices
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    def calcular_coste_total(self):
        items = ItemVenta.objects.filter(venta=self)
        return sum(map(lambda i: i.calcular_coste_por_cantidad(), items))

class ItemVenta(models.Model):
    class Meta():
        verbose_name = "item_venta"
        verbose_name_plural = "items_venta"
        
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, default=None, related_name='items')

    def __str__(self):
        return '{} x {} uds.'.format(self.producto.nombre, self.cantidad)
    
    def calcular_coste_por_cantidad(self):
        return self.producto.precio_base * self.cantidad

class Reclamacion(models.Model):
    class Meta():
        verbose_name = "reclamacion"
        verbose_name_plural = "reclamaciones"

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    resuelta = models.BooleanField(default=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, default=None)
