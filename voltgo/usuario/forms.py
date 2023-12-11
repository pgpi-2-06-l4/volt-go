from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Direccion
import re

class LoginForm(forms.Form):
    email = forms.CharField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña',
                               widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_first_name(self):
        cd = self.cleaned_data['first_name']
        if len(cd) == 0:
            raise forms.ValidationError('La cadena no puede estar vacía')
        if not re.match("^[A-Za-záéíóúüÜñÑ\s]+$", cd):
            raise forms.ValidationError('El nombre no debe incluir números o caracteres especiales.')
        return cd

    def clean_last_name(self):
        cd = self.cleaned_data['last_name']
        if len(cd) == 0:
            raise forms.ValidationError('La cadena no puede estar vacía')
        if not re.match("^[A-Za-záéíóúüÜñÑ\s]+$", cd):
            raise forms.ValidationError('Los apellidos no deben incluir números o caracteres especiales.')
        return cd

    def clean_email(self):
        cd = self.cleaned_data['email']
        if len(cd) == 0:
            raise forms.ValidationError('La dirección de correo no puede estar vacía.')
        if not re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", cd):
            raise forms.ValidationError('La dirección de correo introducida no es válida.')
        return cd
        
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['fecha_nacimiento', 'telefono']
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}),
        }

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'apartamento', 'pais', 'ciudad', 'codigo_postal']


