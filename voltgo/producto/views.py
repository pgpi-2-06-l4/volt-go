from typing import Any
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Producto
from django.shortcuts import render
from .forms import BusquedaForm


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