from django.urls import path
from .views import home_view
from .views import about_view
from .views import checkout
from .views import create_checkout_session

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('checkout/', checkout, name='checkout'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
]