from django.contrib import admin
from .models import *

admin.site.register(Empresa)
admin.site.register(Caracteristica)
admin.site.register(Producto)
admin.site.register(ItemCarrito)
admin.site.register(Comentario)

