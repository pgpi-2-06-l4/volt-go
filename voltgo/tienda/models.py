from django.db import models
from producto.models import Producto
from usuario.models import Usuario

class Venta(models.Model):
    class Meta():
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        
    class EstadoProducto(models.IntegerChoices):
        EN_CARRITO = 0, ('En carrito')
        PENDIENTE = 1, ('Pendiente')
        RESERVADO = 2, ('Reservado')
        FINALIZADO = 3, ('Finalizado')

    class EstadoEnvio(models.IntegerChoices):
        EN_ALMACEN = 0, ('En almacen')
        EN_REPARTO = 1, ('En reparto')
        ENTREGADO = 2, ('Entregado')

    class TipoPago(models.IntegerChoices):
        CONTRAREEMBOLSO = 0, ('Contrareembolso')
        PASARELA = 1, ('Pasarela')
     
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=True)   
    estado_producto = models.IntegerField(
        default=EstadoProducto.EN_CARRITO, 
        choices=EstadoProducto.choices
    )
    estado_envio = models.IntegerField(
        default=EstadoEnvio.EN_ALMACEN,
        choices=EstadoEnvio.choices
    )
    tipo_pago = models.IntegerField(
        default=TipoPago.PASARELA,
        choices=TipoPago.choices
    )
    producto = models.OneToOneField(
        Producto, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE
    )
