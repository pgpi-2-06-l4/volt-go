from django.db import models

class Empresa(models.Model):
    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'

    nombre = models.CharField(max_length=50, null=False, unique=True)
    descripcion = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.nombre
    


class Producto(models.Model):
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    nombre = models.CharField(max_length=50, null=False, unique=True)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    url_imagen = models.URLField(null=False)
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return self.nombre
    

