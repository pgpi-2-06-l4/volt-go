from django.urls import path
from .views import ProductDetailView

urlpatterns = [
    path('<pk>/', ProductDetailView.as_view(), name='detalle-producto')
]