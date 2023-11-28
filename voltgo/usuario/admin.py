from django.contrib import admin
from .models import Usuario, Perfil

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'direction', 'photo']

admin.site.register(Perfil)