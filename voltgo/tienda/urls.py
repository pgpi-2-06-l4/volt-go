from django.urls import path
from .views import *

app_name = 'tienda'

urlpatterns = [
    path('', home_view, name='home'),
    path('gestion/', manage_view, name='manage'),
    path('venta/eliminar/<int:pk>/', eliminar_venta, name="eliminar_venta"),
    path('about/', about_view, name='about'),
    path('checkout/', checkout, name='checkout'),

]