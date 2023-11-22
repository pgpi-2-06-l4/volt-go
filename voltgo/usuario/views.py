from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import LoginForm, UserRegistrationForm
from django.contrib import messages
from django.shortcuts import redirect

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/usuario/dashboard')  # Redirigir a la página principal si ya está autenticado

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    dashboard_url = reverse('dashboard')
                    return HttpResponseRedirect(dashboard_url)
                else:
                    return HttpResponse('Cuenta desactivada')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            # Autenticar al usuario después de registrarse
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '¡Registro exitoso! Ahora estás conectado.')
                
                # Redirigir al usuario al dashboard
                return redirect('dashboard')  # Reemplaza 'dashboard' con la URL de tu dashboard

    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})
