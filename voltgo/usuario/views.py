from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Usuario, Perfil
from .forms import LoginForm, UserRegistrationForm, UserEditForm, UserProfileEditForm
from django.contrib import messages

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
            
            perfil = Perfil(usuario=new_user)
            perfil.save()

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
                messages.error(request, 'Error en la autenticación después del registro.')
        else:
            # Si hay errores en el formulario, los agregamos al contexto
            messages.error(request, 'Corrige los errores marcados en rojo.')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def gestionar_perfil(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user.perfil)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.perfil)

    return render(request, 'account/gestionar_perfil.html', {'user_form': user_form, 'profile_form': profile_form})