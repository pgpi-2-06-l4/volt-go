from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib import messages

from django.conf import settings
from .forms import *
from .models import Venta, Reclamacion, ItemVenta
from usuario.models import *
from producto.models import ItemCarrito

from typing import Any

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
        context['autenticado'] = self.request.user.is_authenticated
        
        form_cliente = InfoPagoClienteForm(request.POST)
        context['form_cliente'] = form_cliente.render(template_form)
        if form_cliente.is_valid():
            self.request.session['form_cliente'] = form_cliente.cleaned_data
            form_cliente_res = InfoPagoClienteForm(initial=form_cliente.cleaned_data)
            context['form_cliente'] = form_cliente_res.render(template_form)
        else:
            context['errores'] = form_cliente.errors
            return render(request, 'info_pago.html', context)
        
        form_direccion = InfoPagoDireccionForm(request.POST)
        context['form_direccion'] = form_direccion.render(template_form)
        if form_direccion.is_valid():
            self.request.session['form_direccion'] = form_direccion.cleaned_data
            form_direccion_res = InfoPagoDireccionForm(initial=form_direccion.cleaned_data)
            context['form_direccion'] = form_direccion_res.render(template_form)
        else:
            context['errores'] = form_direccion.errors
            return render(request, 'info_pago.html', context)

        form_tarjeta = InfoPagoTarjetaForm(request.POST)
        context['form_tarjeta'] = form_tarjeta.render(template_form)
        if form_tarjeta.is_valid():
            form_tarjeta.cleaned_data['caducidad'] = form_tarjeta.cleaned_data['caducidad'].strftime('%d/%m/%Y')
            self.request.session['form_tarjeta'] = form_tarjeta.cleaned_data
            form_tarjeta_res = InfoPagoTarjetaForm(initial=form_tarjeta.cleaned_data)
            context['form_tarjeta'] = form_tarjeta_res.render(template_form)
        else:
            context['errores'] = form_tarjeta.errors
            return render(request, 'info_pago.html', context)
        
        return render(request, 'resumen_pedido.html', context)

class Checkout(View):
    
    def post(self, request):
        usuario = request.user
        sesion_id = None
        if usuario.is_authenticated:
            if usuario.is_superuser:
                return render(request, '403.html')
        else:
            # Usuarios no autenticados
            sesion_id = request.session['user_identifier']
            usuario = None
            
        # Guardamos datos en la sesión
        info_cliente = {}
        form_cliente = InfoPagoClienteForm(request.POST)
        if form_cliente.is_valid():
            info_cliente.update(form_cliente.cleaned_data)
        form_dir = InfoPagoDireccionForm(request.POST)           
        if form_dir.is_valid():
            info_cliente.update(form_dir.cleaned_data)
        form_tarjeta = InfoPagoTarjetaForm(request.POST)
        if form_tarjeta.is_valid():
            form_tarjeta.cleaned_data['caducidad'] = form_tarjeta.cleaned_data['caducidad'].strftime('%d/%m/%Y')
            info_cliente.update()
        request.session['info_cliente'] = info_cliente
            
        estado_venta = Venta.EstadoVenta.POR_PAGAR
        estado_envio = Venta.EstadoEnvio.EN_ALMACEN
        tipo_pago = int(request.POST.get('tipo_pago'))
        
        venta = Venta(
            fecha_inicio=timezone.now(),
            fecha_fin=None,
            estado_venta=estado_venta,
            estado_envio=estado_envio,
            tipo_pago=tipo_pago,
            usuario=usuario,
            sesion_id=sesion_id
        )
        venta.save()

        # Reservar unidades de producto para cliente y crear venta
        for item_id in self.request.session.get('items'):
            item = ItemCarrito.objects.get(pk=item_id)
            if item.producto.stock - item.cantidad >= 0:
                item.producto.stock -= item.cantidad
                item.producto.save()
            else:
                venta.delete()
                return render(request, '403.html')
            
        if tipo_pago == 1:   
            # Pasarela de pago

            # TODO                    
            
            # Actualizamos estado venta
            venta.fecha_fin = timezone.now()
            venta.estado_venta = Venta.EstadoVenta.PAGADO
            venta.save()
        
        # Si todo sale bien, eliminamos items del carrito 
        # y creamos items de la venta
        items_venta = []
        for item_id in request.session.get('items'):
            item_carrito = ItemCarrito.objects.get(pk=item_id)

            item_venta = ItemVenta(
                producto=item_carrito.producto,
                cantidad=item_carrito.cantidad,
                venta=venta
            )
            
            item_venta.save()
            items_venta.append(item_venta)
            item_carrito.delete()

        self.enviar_correo_compra(venta, items_venta)
        request.session.flush()
        messages.success(request, 'Se ha enviado un correo a tu cuenta.')
        return redirect('home')
        
    def enviar_correo_compra(self, venta, items):
        cliente = self.request.session['info_cliente']
        ASUNTO = 'VoltGo - Ticket compra {}'.format(venta.fecha_inicio.strftime('%d/%m/%Y %H:%M'))
        MENSAJE = """Hola {nombre}, aquí tienes el resumen de tu compra:\n
        {articulos}
        ------------------------------------
        TIPO DE PAGO: {tipo_pago}
        TOTAL: {total} €
        
        Dirección de envío: {direccion}
                
        ¡Gracias por tu compra!
        
        Atentamente,
        VoltGo.
        """.format(
            nombre=cliente['nombre'],
            articulos='\n\t'.join([str(item) for item in items]),
            tipo_pago=venta.get_tipo_pago_display(),
            total=venta.calcular_coste_total(),
            direccion=f"{cliente['calle']},{cliente['apartamento']},{cliente['ciudad']},{cliente['pais']}"
        )
        REMITENTE = settings.EMAIL_HOST_USER
        DESTINATARIO = [cliente['email']]
        
        email = EmailMessage(
            ASUNTO,
            MENSAJE,
            REMITENTE,
            DESTINATARIO
        )
        email.fail_silently = False
        email.send()
    
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
    compras = Venta.objects.filter(usuario=request.user)
    items_compra = {}
    for compra in compras:
        if compra.id in items_compra:
            continue
        else:
            items_compra[compra.id] = compra.items.all()
    return render(request, 'compras_by_user.html', {'compras': compras, 'items_compra': items_compra})

