from django.urls import path
from .views import home_view, eliminar_venta, about_view, InfoPago, ResumenPedido, Checkout, reclamacion_view, reclamaciones_by_user, compras_by_user, success, seguimiento, obtener_cantidad_carrito

app_name = 'tienda'

urlpatterns = [
    path('', home_view, name='home'),
    path('venta/eliminar/<int:pk>/', eliminar_venta, name="eliminar_venta"),
    path('about/', about_view, name='about'),
    path('info-pago/', InfoPago.as_view(), name='info-pago'),
    path('resumen-pedido/', ResumenPedido.as_view(), name='resumen-pedido'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('reclamacion/<int:pk>/', reclamacion_view, name='reclamacion'),
    path('reclamaciones/', reclamaciones_by_user, name='reclamaciones'),
    path('compras/', compras_by_user, name='compras'),  
    path('success/', success, name='success') , 
    path('seguimiento/', seguimiento, name='seguimiento'),
    path('obtenerNumCarrito/', obtener_cantidad_carrito, name='obtenerNumCarrito'),
]

