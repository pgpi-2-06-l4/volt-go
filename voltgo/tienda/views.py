from django.shortcuts import render
from .models import Venta
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from producto.models import ItemCarrito

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
    if request.method == 'GET':
        context = {}
        items = [ItemCarrito.objects.get(pk=i) for i in request.session.get('items')]
        
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
        
        return render(request, 'checkout.html', context)
    elif request.method == 'POST':
        #TODO - PASARELA DE PAGO CON SPRITE
        return redirect('')