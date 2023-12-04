from django.db import models
from usuario.models import Usuario

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
        Usuario,
        on_delete=models.CASCADE
    )


class Reclamacion(models.Model):
    class Meta():
        verbose_name = "reclamacion"
        verbose_name_plural = "reclamaciones"

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    resuelta = models.BooleanField(default=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, default=None)
