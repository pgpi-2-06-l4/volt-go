from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

from .forms import *
from .models import Venta, Reclamacion, ItemVenta
from usuario.models import *
from producto.models import ItemCarrito

import stripe
from typing import Any
from django.http import JsonResponse

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
            
            info_pago_cliente = InfoPagoClienteForm(initial=datos_usuario)
            info_pago_direccion = InfoPagoDireccionForm(initial=datos_direccion)
            
        else:
            context['autenticado'] = False
            info_pago_cliente = InfoPagoClienteForm()
            info_pago_direccion = InfoPagoDireccionForm()

        info_tipo_pago = InfoTipoPagoForm()
        template_form = 'info_pago_form.html'
        context['form_cliente'] = info_pago_cliente.render(template_form)
        context['form_direccion'] = info_pago_direccion.render(template_form)
        context['form_tarjeta'] = info_tipo_pago.render(template_form)
        
        return context
    
    
class ResumenPedido(TemplateView):
    template_name = 'resumen_pedido.html'
    
    def get_context_data(self, **kwargs):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
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
        context['stripe_public_key'] = stripe_public_key

        return context

    def post(self, request):
        context = self.get_context_data()
        template_form = 'info_pago_form.html'
        context['autenticado'] = self.request.user.is_authenticated
        
        info_cliente = {}
        form_cliente = InfoPagoClienteForm(request.POST)
        context['form_cliente'] = form_cliente.render(template_form)
        if form_cliente.is_valid():
            self.request.session['form_cliente'] = form_cliente.cleaned_data
            form_cliente_res = InfoPagoClienteForm(initial=form_cliente.cleaned_data, disabled=True)
            context['form_cliente'] = form_cliente_res.render(template_form)
            info_cliente.update(form_cliente.cleaned_data)
            print(info_cliente)
        else:
            context['errores'] = form_cliente.errors
            return render(request, 'info_pago.html', context)
        
        form_direccion = InfoPagoDireccionForm(request.POST)
        context['form_direccion'] = form_direccion.render(template_form)
        if form_direccion.is_valid():
            self.request.session['form_direccion'] = form_direccion.cleaned_data
            form_direccion_res = InfoPagoDireccionForm(initial=form_direccion.cleaned_data, disabled=True)
            context['form_direccion'] = form_direccion_res.render(template_form)
            info_cliente.update(form_direccion.cleaned_data)
        else:
            context['errores'] = form_direccion.errors
            return render(request, 'info_pago.html', context)

        form_tipo_pago = InfoTipoPagoForm(request.POST)
        context['form_tipo_pago'] = form_tipo_pago.render(template_form)
        if form_tipo_pago.is_valid():
            self.request.session['form_tipo_pago'] = form_tipo_pago.cleaned_data
            form_tipo_pago_res = InfoTipoPagoForm(initial=form_tipo_pago.cleaned_data, disabled=True)
            context['form_tipo_pago'] = form_tipo_pago_res.render(template_form)
            info_cliente.update(form_tipo_pago.cleaned_data)
        else:
            context['errores'] = form_tipo_pago.errors
            return render(request, 'info_pago.html', context)
        
        request.session['info_cliente'] = info_cliente
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
            
        estado_venta = Venta.EstadoVenta.POR_PAGAR
        estado_envio = Venta.EstadoEnvio.EN_ALMACEN
        info_cliente = request.session['info_cliente']
        tipo_pago = int(info_cliente['tipo_pago'])

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
        request.session["venta_id"] = venta.id

        # Reservar unidades de producto para cliente y crear venta
        for item_id in self.request.session.get('items'):
            item = ItemCarrito.objects.get(pk=item_id)
            if item.producto.stock - item.cantidad >= 0:
                item.producto.stock -= item.cantidad
                item.producto.save()
            else:
                venta.delete()
                return render(request, '403.html')   
        # Pasarela de pago
        if tipo_pago == 1:   
            try:
                customer_email = info_cliente["email"]
                items_id = self.request.session.get('items')
                line_items = []
                precio_total_items = 0
                for item_id in items_id:
                    item = ItemCarrito.objects.get(pk=item_id)
                    precio_total_items += item.producto.precio_base * item.cantidad
                    producto = stripe.Product.create(
                        name = item.producto.nombre,
                        description = item.producto.descripcion,
                        images=[item.producto.url_imagen]
                    )
                    
                    precio = stripe.Price.create(
                        unit_amount=int(item.producto.precio_base * 100),
                        currency= "eur",
                        product= producto.id,
                    )
          
                    line_items.append({
                        'price': precio.id,
                        "quantity": item.cantidad,
                    })
                
                if precio_total_items < 50:
                    line_items.append({
                        'price_data': {
                        'currency': 'eur',
                        'unit_amount': int(5.00 * 100),
                        'product_data': {
                            'name': 'Tasa de envío',
                            'description': 'Monto de envío',
                            },
                        },
                    'quantity': 1,
                    })
              
                stripe.api_key = settings.STRIPE_SECRET_KEY
                request.session['payment_processed'] = False

                session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items= line_items,
                    mode='payment',
                    customer_email= customer_email,
                    success_url=request.build_absolute_uri('/tienda/success/'),
                    cancel_url=request.build_absolute_uri('/tienda/info-pago/'),
                )
                # print("ID de la sesión creada:", session.id)
                request.session['stripe_session_id'] = session.id
                return redirect(session.url)
            except stripe.error.StripeError as e:
                # print("Error al crear la sesión de pago:", str(e))
                return JsonResponse({'error': str(e)}, status=400)
        return redirect("tienda:success")
        
    
    
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
    if (not request.user.is_authenticated):
        return redirect('/home')
    reclamaciones = Reclamacion.objects.filter(venta__usuario=request.user)
    return render(request, 'reclamaciones_by_user.html', {'reclamaciones': reclamaciones})

def compras_by_user(request):
    if (not request.user.is_authenticated):
        return redirect('/home')
    compras = Venta.objects.filter(usuario=request.user)
    items_compra = {}
    for compra in compras:
        if compra.id in items_compra:
            continue
        else:
            items_compra[compra.id] = compra.items.all()
    return render(request, 'compras_by_user.html', {'compras': compras, 'items_compra': items_compra})

def enviar_correo_compra(request, venta, items):
        cliente = request.session['info_cliente']
        ASUNTO = 'VoltGo - Ticket compra {}'.format(venta.fecha_inicio.strftime('%d/%m/%Y %H:%M'))
        total = venta.calcular_coste_total()
        envio = 5 if total < 50 else 0
        total = total + envio if envio else total
        MENSAJE = """Hola {nombre}, aquí tienes el resumen de tu compra:\n
        {articulos}
        ------------------------------------
        TIPO DE PAGO: {tipo_pago}
        ENVÍO: {envio} €
        TOTAL: {total} €
        
        Dirección de envío: {direccion}
        ID del pedido: {id_pedido} 
        ¡Gracias por tu compra!
        
        Atentamente,
        VoltGo.
        """.format(
            nombre=cliente['nombre'],
            articulos='\n\t'.join([str(item) for item in items]),
            tipo_pago=venta.get_tipo_pago_display(),
            envio=envio,
            total=total,
            direccion=f"{cliente['calle']},{cliente['apartamento']},{cliente['ciudad']},{cliente['pais']}",
            id_pedido= venta.id
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

def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY  

    session_id = request.session.get('stripe_session_id')
    info_cliente = request.session['info_cliente'] 
  
    tipoPago = int(info_cliente["tipo_pago"])

    venta_id = request.session.get("venta_id")
    if venta_id is not None:
        venta = Venta.objects.get(pk=venta_id)
        print(venta)
    else:
    # Manejar el caso cuando venta_id es None
        print("Error: venta_id no encontrado en la sesión.")

    if(tipoPago == 1): 
        if session_id:
            if not request.session.get('payment_processed'):
                try:
                    session = stripe.checkout.Session.retrieve(session_id)
                    payment_intent_id = session.payment_intent
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    estado_pago = payment_intent.status

                    print("ID de sesión de pago:", session.id)
                    print("Situación del pago:", estado_pago)

                    if estado_pago == "succeeded":
                        print("El pago se ha completado con éxito.")
                        request.session['payment_processed'] = True
                        # Actualizamos estado venta 
                        venta.tipo_pago = Venta.TipoPago.PASARELA
                        venta.estado_venta = Venta.EstadoVenta.PAGADO
                        venta.fecha_fin = timezone.now()
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

                        enviar_correo_compra(request, venta, items_venta)
                        messages.success(request, 'Se ha enviado un correo a tu cuenta.')
                        return render(request, 'success.html')
                    else:
                        print("Error: El pago no se ha completado.")
                except stripe.error.StripeError as e:
                    print("Error al recuperar la sesión de pago:", str(e))
            else:
                print("Error: La sesión ya ha sido procesada.")
        else:
            print("Error: No se encontró información de pago en la sesión.")
    else:
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
        
        venta.tipo_pago = Venta.TipoPago.CONTRAREEMBOLSO
        venta.fecha_fin = timezone.now()
        venta.save()
        enviar_correo_compra(request, venta, items_venta)
        messages.success(request, 'Se ha enviado un correo a tu cuenta.')
        print('El pago se realizará contrareembolso.')
        return render(request, 'success.html')
        
def seguimiento(request):
    resultado_pedido = None
    mensaje_error = None

    if request.method == 'POST':
        form = BuscarPedidoForm(request.POST)

        if form.is_valid():
            id_pedido = form.cleaned_data['id_pedido']
            resultado_pedido = Venta.objects.filter(pk=id_pedido).first()

            if not resultado_pedido:
                mensaje_error = "No se encontró ningún pedido con ese ID."

    else:
        form = BuscarPedidoForm()

    return render(request, 'seguimiento.html', {'form': form, 'resultado_pedido': resultado_pedido, 'mensaje_error': mensaje_error})


def obtener_cantidad_carrito(request):
    if request.user.is_authenticated:
        cantidad_carrito = ItemCarrito.objects.filter(usuario=request.user).count()
        return JsonResponse({'cantidad_carrito': cantidad_carrito})
    else:
        return JsonResponse({'error': 'Usuario no autenticado'})