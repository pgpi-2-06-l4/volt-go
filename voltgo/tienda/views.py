from django.shortcuts import render
from .models import Venta
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def home_view(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='/')
def manage_view(request):
    ventas = Venta.objects.all()
    return render(request, 'manage.html', {'ventas': ventas})

def eliminar_venta(request, pk):
    venta = Venta.objects.get(pk=pk)
    venta.delete()
    return redirect('tienda:manage')

def about_view(request):
    return render(request, 'about.html')

def checkout(request):
    context = {}
    productos = []
    
    return render(request, 'checkout.html')