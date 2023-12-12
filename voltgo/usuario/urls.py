from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/usuario/login/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('gestionar_perfil/', views.gestionar_perfil, name='gestionar_perfil'),
    path('direccion/<int:pk>/eliminar/', views.eliminar_direccion, name='eliminar_direccion'),
    path('direccion/editar/<int:pk>/', views.direccion_editar, name='direccion_editar'),
    path('direccion/nueva/', views.direccion_editar, name='direccion_nueva'),
]
