from django.contrib import admin
from producto.models import Empresa, Caracteristica, Producto, ItemCarrito

admin.site.register(Empresa)
admin.site.register(Caracteristica)
admin.site.register(Producto)
admin.site.register(ItemCarrito)
