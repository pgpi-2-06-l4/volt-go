from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', LogoutView.as_view(next_page='/usuario/login'), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    # path('edit', views.edit, name='edit'),
    path('', include('django.contrib.auth.urls')),
    path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    path('password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('gestionar_perfil/', views.gestionar_perfil, name='gestionar_perfil'),
    path('direccion/<int:pk>/eliminar/', views.eliminar_direccion, name='eliminar_direccion'),
    path('direccion/editar/<int:pk>/', views.direccion_editar, name='direccion_editar'),
    path('direccion/nueva/', views.direccion_editar, name='direccion_nueva'),
    path('tarjeta/<int:pk>/eliminar/', views.eliminar_tarjeta, name='eliminar_tarjeta'),
    path('tarjeta/editar/<int:pk>/', views.tarjeta_editar, name='tarjeta_editar'),
    path('tarjeta/nueva/', views.tarjeta_editar, name='tarjeta_nueva'),
]
