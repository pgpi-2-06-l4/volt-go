from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from .models import Venta
from producto.models import ItemCarrito
from usuario.models import *
from typing import Any
from .forms import *

def home_view(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='/')
def manage_view(request):
    ventas = Venta.objects.all()
    return render(request, 'manage.html', {'ventas': ventas})

def eliminar_venta(request, pk):
    venta = Venta.objects.get(pk=pk)
    venta.delete()
    return redirect('tienda:manage')

def about_view(request):
    return render(request, 'about.html')


class InfoPago(TemplateView):
    template_name = 'info_pago.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        datos_usuario = {}
        
        if self.request.user.is_authenticated:
            context['autenticado'] = True

            usuario = User.objects.get(pk=self.request.user.pk)
            perfil,_ = Perfil.objects.get_or_create(usuario=usuario)
            direccion,_ = Direccion.objects.get_or_create(usuario=usuario)
            tarjeta,_ = TarjetaCredito.objects.get_or_create(usuario=usuario)
            
            datos_usuario = {
                'nombre': usuario.first_name + ' ' + usuario.last_name,
                'email': usuario.email,
                'telefono': perfil.telefono
            }
            datos_direccion = {
                'calle': direccion.calle,
                'apartamento': direccion.apartamento,
                'pais': direccion.pais,
                'ciudad': direccion.ciudad,
                'codigo_postal': direccion.codigo_postal
            }
            datos_tarjeta = { 
                'iban': tarjeta.iban,
                'caducidad': tarjeta.fecha_caducidad,
                'cvv': tarjeta.cvv
            }
            
            info_pago_cliente = InfoPagoClienteForm(initial=datos_usuario)
            info_pago_direccion = InfoPagoDireccionForm(initial=datos_direccion)
            info_pago_tarjeta = InfoPagoTarjetaForm(initial=datos_tarjeta)
            
        else:
            context['autenticado'] = False
            info_pago_cliente = InfoPagoClienteForm()
            info_pago_direccion = InfoPagoDireccionForm()
            info_pago_tarjeta = InfoPagoTarjetaForm()

        template_form = 'info_pago_form.html'
        context['form_cliente'] = info_pago_cliente.render(template_form)
        context['form_direccion'] = info_pago_direccion.render(template_form)
        context['form_tarjeta'] = info_pago_tarjeta.render(template_form)
        
        return context
    
    def post(self, request):
        context = self.get_context_data()
        self.request.session['info_pago'] = {
            'nombre': context['nombre'],
            'email': context['email'],
            'tel': context['perfil'].telefono,
            'direccion': {
                'calle': context['direccion'].calle,
                'apartamento': context['direccion'].apartamento,
                'pais': context['direccion'].pais,
                'ciudad': context['direccion'].ciudad,
                'codigo_postal': context['direccion'].codigo_postal,
            },
            'tarjeta': {
                'iban': context['tarjeta'].iban,
                'fecha_caducidad': context['tarjeta'].fecha_caducidad,
                'cvv': context['tarjeta'].cvv
            }
        }
        
        return super().post(request, context)
    
class ResumenPedido(TemplateView):
    template_name = 'resumen_pedido.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        items = [ItemCarrito.objects.get(pk=i)
                 for i in self.request.session.get('items')]
        
        envio = 5
        total = 0
        pedido = 0
        for item in items:
            pedido += item.producto.precio_base * item.cantidad
        
        if pedido < 50:
            total = envio + pedido
            context['envio'] = envio
        else:
            total = pedido
            context['envio'] = 0
        
        context['items'] = items
        context['pedido'] = pedido
        context['total'] = total
        context['info_pago'] = self.request.session.get('info_pago')
        
        return context
    
    def post(self, request):
        return render(request, 'resumen_pedido.html', self.get_context_data())

class Checkout(View):
    
    def post(self, request):
        #TODO - PASARELA DE PAGO CON SPRITE
        return redirect('')
