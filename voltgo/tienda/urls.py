from django.urls import path
from .views import home_view
from .views import manage_view
from .views import eliminar_venta
from .views import about_view
from .views import checkout
from .views import create_checkout_session

app_name = 'tienda'

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('checkout/', checkout, name='checkout'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('gestion/', manage_view, name='manage'),
    path('venta/eliminar/<int:pk>/', eliminar_venta, name="eliminar_venta"),
]