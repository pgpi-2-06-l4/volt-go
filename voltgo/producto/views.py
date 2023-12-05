from typing import Any
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Producto, ItemCarrito, Comentario
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BusquedaForm, ComentarioForm
from urllib.parse import urlencode
from collections import defaultdict
import uuid

class ProductDetailView(DetailView):
    model = Producto
    template_name = "detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.get_object()
        comentarios = Comentario.objects.filter(producto=producto)
        context['comentarios'] = comentarios
        context['formulario_comentario'] = ComentarioForm()
        return context

    def post(self, request, *args, **kwargs):
        producto = self.get_object()
        formulario_comentario = ComentarioForm(request.POST)

        if formulario_comentario.is_valid():
            comentario = formulario_comentario.save(commit=False)
            comentario.producto = producto
            comentario.usuario = request.user
            comentario.save()

        return redirect('catalogo')

def catalogo(request):
    form = BusquedaForm(request.GET)
    productos = Producto.objects.all()

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        empresa = form.cleaned_data.get('empresa')
        precio_maximo = form.cleaned_data.get('precio_maximo')

        if nombre:
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
    producto = Producto.objects.get(pk=pk)

    if request.user.is_authenticated:
        item, es_nuevo = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    else:
        user_identifier = str(uuid.uuid5(uuid.NAMESPACE_DNS, request.META['REMOTE_ADDR']))
        request.session['user_identifier'] = user_identifier
        item, es_nuevo = ItemCarrito.objects.get_or_create(session_id=user_identifier, producto=producto)
    
    item.cantidad = cantidad if es_nuevo else item.cantidad + 1
    item.save()
    return redirect('carrito')
    
def eliminar_del_carrito(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.user.is_authenticated:
        item = ItemCarrito.objects.get(usuario=request.user, producto=producto)
    else:
        user_identifier = str(uuid.uuid5(uuid.NAMESPACE_DNS, request.META['REMOTE_ADDR']))
        request.session['user_identifier'] = user_identifier
        item = ItemCarrito.objects.get(session_id=user_identifier, producto=producto)
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
        clave = str(uuid.uuid5(uuid.NAMESPACE_DNS, request.META['REMOTE_ADDR']))
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
