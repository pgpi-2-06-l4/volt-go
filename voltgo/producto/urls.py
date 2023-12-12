from django.urls import path
from .views import catalogo, ProductDetailView, ver_carrito, agregar_al_carrito, eliminar_del_carrito, vaciar_carrito, pagar_carrito

app_name = 'producto'

urlpatterns = [
    path('catalogo/', catalogo, name='catalogo'),
    path('<pk>/', ProductDetailView.as_view(), name='detalle-producto'),
    path('catalogo/carrito/', ver_carrito, name='carrito'),
    path('catalogo/carrito/add-producto/<int:pk>/', agregar_al_carrito, name='agregar-al-carrito'),
    path('catalogo/carrito/del-carrito/<int:pk>/', eliminar_del_carrito, name='eliminar-del-carrito'),
    path('catalogo/carrito/del-entero', vaciar_carrito, name='vaciar-carrito'),
    path('catalogo/carrito/pagar/', pagar_carrito, name='pagar-carrito'),
]