from django.urls import path
from .views import home_view
from .views import manage_view
from .views import eliminar_venta
from .views import about_view

app_name = 'tienda'

urlpatterns = [
    path('', home_view, name='home'),
    path('gestion/', manage_view, name='manage'),
    path('venta/eliminar/<int:pk>/', eliminar_venta, name="eliminar_venta"),
    path('about/', about_view, name='about'),
]