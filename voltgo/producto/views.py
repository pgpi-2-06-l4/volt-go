from typing import Any
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Producto, ItemCarrito
from django.shortcuts import render, redirect
from .forms import BusquedaForm
from urllib.parse import urlencode


class ProductDetailView(DetailView):
    model = Producto
    template_name = "detalle.html"

def catalogo(request):

    form = BusquedaForm(request.GET)
    productos = Producto.objects.all()
    productos_con_caracteristicas = []

    if form.is_valid():
        autonomia = form.cleaned_data.get('autonomia')
        velocidad_maxima = form.cleaned_data.get('velocidad_maxima')
        precio_maximo = form.cleaned_data.get('precio_maximo')

        if autonomia is not None:
            productos = productos.filter(caracteristicas__nombre='AT', caracteristicas__valor__gte=int(autonomia))

        if velocidad_maxima is not None:
            productos = productos.filter(caracteristicas__nombre='VM', caracteristicas__valor__lte=int(velocidad_maxima))

        if precio_maximo is not None:
            productos = productos.filter(precio_base__lte=float(precio_maximo))

    for producto in productos:
        autonomia = producto.caracteristicas.filter(nombre='AT').first()
        velocidad_maxima = producto.caracteristicas.filter(nombre='VM').first()

        autonomia_valor = autonomia.valor if autonomia else '0'
        velocidad_maxima_valor = velocidad_maxima.valor if velocidad_maxima else '0'
        

        producto_dict = {
            'producto': producto,
            'autonomia': autonomia_valor,
            'velocidad_maxima': velocidad_maxima_valor,
        }
        productos_con_caracteristicas.append(producto_dict)
    
    return render(request, 'catalogo.html', {'productos': productos_con_caracteristicas, 'form':form})

def agregar_al_carrito(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.user.is_authenticated:
        item, creado = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    else:
        session_key = request.session.session_key
        item, creado = ItemCarrito.objects.get_or_create(session_id=session_key, producto=producto)
    
    if not creado:
        item.cantidad += 1
        item.save()
    return redirect('carrito')
    
def eliminar_del_carrito(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.user.is_authenticated:
        item = ItemCarrito.objects.get(usuario=request.user, producto=producto)
    else:
        session_key = request.session.session_key
        item = ItemCarrito.objects.get(session_id=session_key, producto=producto)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return ver_carrito(request)

def ver_carrito(request):
    if request.user.is_authenticated:
        clave = request.user
    else:
        clave = request.session.session_key
    carrito = []
    total = 0
    for item in ItemCarrito.objects.all():
        if item.usuario == clave or item.session_id == clave:
            carrito.append(item)
            total += item.producto.precio_base * item.cantidad
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

def vaciar_carrito(request):
    if request.user.is_authenticated:
        clave = request.user
    else:
        clave = request.session.session_key
    carrito = []
    for item in ItemCarrito.objects.all():
        if item.usuario == clave or item.session_id == clave:
            item.delete()
    return ver_carrito(request)

def pagar_carrito(request):
    if request.method == 'POST':
        request.session['items'] = request.POST.getlist('item[]')
        return redirect('/tienda/info-pago/')
    else:
        return redirect('/productos/catalogo/carrito/')