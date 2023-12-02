from django.shortcuts import render
from .models import Venta
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from producto.models import ItemCarrito
from django.shortcuts import get_object_or_404
from .forms import ReclamacionForm
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


    