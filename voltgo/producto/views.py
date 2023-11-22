from typing import Any
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Producto
from django.shortcuts import render


class ProductDetailView(DetailView):
    model = Producto
    template_name = "detalle.html"

def catalogo(request):
    productos = Producto.objects.all()
    productos_con_caracteristicas = []
    for producto in productos:
        autonomia = producto.caracteristicas.filter(nombre='AT').first()
        velocidad_maxima = producto.caracteristicas.filter(nombre='VM').first()

        autonomia_valor = autonomia.valor if autonomia else 'No disponible'
        velocidad_maxima_valor = velocidad_maxima.valor if velocidad_maxima else 'No disponible'
        

        producto_dict = {
            'producto': producto,
            'autonomia': autonomia_valor,
            'velocidad_maxima': velocidad_maxima_valor,
        }
        productos_con_caracteristicas.append(producto_dict)
    
    return render(request, 'catalogo.html', {'productos': productos_con_caracteristicas})