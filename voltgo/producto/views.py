from typing import Any
from django.views.generic.detail import DetailView
from .models import Producto


class ProductDetailView(DetailView):
    model = Producto
    template_name = "detalle.html"
