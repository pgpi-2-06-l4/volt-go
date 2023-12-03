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
from django.shortcuts import get_object_or_404
from .models import Reclamacion

def home_view(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_staff

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
    
    
class ResumenPedido(TemplateView):
    template_name = 'resumen_pedido.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_id = self.request.session.get('items')
        items = []
        for item_id in items_id:
            item = ItemCarrito.objects.get(pk=item_id)
            items.append(item)
            
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
        
        return context

    def post(self, request):
        context = self.get_context_data()
        template_form = 'info_pago_form.html'
        
        form_cliente = InfoPagoClienteForm(request.POST)
        if form_cliente.is_valid():
            self.request.session['form_cliente'] = form_cliente.cleaned_data
            form_cliente_res = InfoPagoClienteForm(initial=form_cliente.cleaned_data)
            context['form_cliente'] = form_cliente_res.render(template_form)
        
        form_direccion = InfoPagoDireccionForm(request.POST)
        if form_direccion.is_valid():
            self.request.session['form_direccion'] = form_direccion.cleaned_data
            form_direccion_res = InfoPagoDireccionForm(initial=form_direccion.cleaned_data)
            context['form_direccion'] = form_direccion_res.render(template_form)

        form_tarjeta = InfoPagoTarjetaForm(request.POST)
        if form_tarjeta.is_valid():
            form_tarjeta.cleaned_data['caducidad'] = form_tarjeta.cleaned_data['caducidad'].strftime('%d/%m/%Y')
            self.request.session['form_tarjeta'] = form_tarjeta.cleaned_data
            form_tarjeta_res = InfoPagoTarjetaForm(initial=form_tarjeta.cleaned_data)
            context['form_tarjeta'] = form_tarjeta_res.render(template_form)
        
        return render(request, 'resumen_pedido.html', context)

class Checkout(View):
    
    def post(self, request):
        #TODO - PASARELA DE PAGO CON SPRITE
        return redirect('')
    
def reclamacion_view(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    form = ReclamacionForm()

    if request.method == 'POST':
        form = ReclamacionForm(request.POST)
        if form.is_valid():
            reclamacion = form.save(commit=False)
            reclamacion.venta = venta
            reclamacion.resuelta = False
            reclamacion.save()
            return render(request, 'reclamacion_exitosa.html', {'venta': venta, 'reclamacion': reclamacion})

    return render(request, 'reclamation.html', {'venta': venta, 'form': form})


def reclamaciones_by_user(request):
    reclamaciones = Reclamacion.objects.filter(venta__usuario__user__username=request.user.username)
    return render(request, 'reclamaciones_by_user.html', {'reclamaciones': reclamaciones})

def compras_by_user(request):
    compras = Venta.objects.filter(usuario__user__username=request.user.username)
    return render(request, 'compras_by_user.html', {'compras': compras})

