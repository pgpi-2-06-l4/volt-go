from django.contrib import admin
from .models import Usuario, Perfil, Direccion, TarjetaCredito

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'direction', 'photo']

admin.site.register(Perfil)
admin.site.register(Direccion)
admin.site.register(TarjetaCredito)