from django.urls import path
from .views import ProductDetailView, catalogo

urlpatterns = [
    path('catalogo/', catalogo, name='catalogo'),
    path('<pk>/', ProductDetailView.as_view(), name='detalle-producto')
    
]