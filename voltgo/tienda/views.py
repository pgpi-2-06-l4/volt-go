from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Venta
from django.contrib.auth.decorators import user_passes_test
import stripe


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

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    return render(request, 'checkout.html', {'stripe_public_key': stripe_public_key})

def create_checkout_session(request):
    print("Recibida solicitud de creación de sesión de pago.")
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1OHsTbGXSBM20rPRUq0KJ0OR',
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/checkout/'),
        )
        print("ID de la sesión creada:", session.id)
        return JsonResponse({'id': session.id})
    except stripe.error.StripeError as e:
        print("Error al crear la sesión de pago:", str(e))
        return JsonResponse({'error': str(e)}, status=400)
