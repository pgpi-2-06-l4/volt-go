import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from .models import Venta
from producto.models import ItemCarrito
from producto.views import vaciar_carrito
from usuario.models import *
from typing import Any
from .forms import *
from django.shortcuts import get_object_or_404
from .models import Reclamacion
import stripe
from django.conf import settings
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
            print("Recibida solicitud de creación de sesión de pago.")
            try:
                payload = json.loads(request.body.decode('utf-8'))
                customer_email = payload.get('email')
                referer_url = payload.get('refererUrl')
                print(referer_url)
                items_id = self.request.session.get('items')
                line_items = []
                precio_total_items = 0
                for item_id in items_id:
                    item = ItemCarrito.objects.get(pk=item_id)
                    precio_total_items += item.producto.precio_base * item.cantidad
                    print(item.producto.url_imagen)
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
                    invoice_creation={"enabled": True},
                    success_url=request.build_absolute_uri('/tienda/success/'),
                    cancel_url=referer_url,
                )

                print("ID de la sesión creada:", session.id)
                request.session['stripe_session_id'] = session.id
                return JsonResponse({'id': session.id})
            except stripe.error.StripeError as e:
                print("Error al crear la sesión de pago:", str(e))
                return JsonResponse({'error': str(e)}, status=400)
    
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

def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY  

    session_id = request.session.get('stripe_session_id')

    objeto = request.session.get('payment_processed')
    print(objeto)

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
                    usuario_actual = Usuario.objects.get(user=request.user)
                    items_id = request.session.get('items')
                    for item_id in items_id:
                        item = ItemCarrito.objects.get(pk=item_id)

                        venta = Venta.objects.create(
                            fecha_inicio=timezone.now(),
                            estado_producto=Venta.EstadoProducto.RESERVADO,
                            estado_envio=Venta.EstadoEnvio.EN_ALMACEN,
                            tipo_pago=Venta.TipoPago.PASARELA,
                            producto=item.producto,
                            usuario=usuario_actual
                        )
                    request.session['payment_processed'] = True
                    vaciar_carrito(request)
                    return render(request, 'success.html')
                else:
                    print("Error: El pago no se ha completado.")
            except stripe.error.StripeError as e:
                print("Error al recuperar la sesión de pago:", str(e))
        else:
            print("Error: La sesión ya ha sido procesada.")
    else:
        print("Error: No se encontró información de pago en la sesión.")
