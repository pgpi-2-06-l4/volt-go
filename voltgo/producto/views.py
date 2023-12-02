from typing import Any
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Producto, ItemCarrito
from django.shortcuts import render, redirect
from .forms import BusquedaForm
from urllib.parse import urlencode
from collections import defaultdict


class ProductDetailView(DetailView):
    model = Producto
    template_name = "detalle.html"

def catalogo(request):
    form = BusquedaForm(request.GET)
    productos = Producto.objects.all()
    productos_con_caracteristicas = []

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        empresa = form.cleaned_data.get('empresa')
        precio_maximo = form.cleaned_data.get('precio_maximo')

        if nombre:
            # Cambia exact por icontains para búsqueda parcial
            productos = productos.filter(nombre__icontains=nombre)

        if empresa:
            productos = productos.filter(empresa__icontains=empresa)

        if precio_maximo is not None:
            productos = productos.filter(precio_base__lte=float(precio_maximo))

    productos_por_empresa = defaultdict(list)

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
        productos_por_empresa[producto.empresa].append(producto_dict)

    return render(request, 'catalogo.html', {'productos_por_empresa': dict(productos_por_empresa), 'form': form})

def agregar_al_carrito(request, pk):
    
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        print('cantidad ' + str(cantidad))
    producto = Producto.objects.get(pk=pk)

    if request.user.is_authenticated:
        item, creado = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    else:
        session_key = request.session.session_key
        item, creado = ItemCarrito.objects.get_or_create(session_id=session_key, producto=producto)
        
    print('item cantidad: ' + str(item.cantidad))
    
    item.cantidad = cantidad if creado else item.cantidad + 1
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
        items = request.POST.getlist('item[]')
        request.session['items'] = items
        return redirect('/tienda/checkout/')
    else:
        return redirect('/productos/catalogo/carrito/')