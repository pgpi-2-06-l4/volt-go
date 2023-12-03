from django.contrib import admin
from .models import *
from producto.models import Caracteristica, Producto, ItemCarrito

admin.site.register(Caracteristica)
admin.site.register(Producto)
admin.site.register(ItemCarrito)
admin.site.register(Comentario)

