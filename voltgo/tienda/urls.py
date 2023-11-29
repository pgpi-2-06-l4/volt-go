from django.urls import path
from .views import home_view
from .views import about_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about')
]