# Generated by Django 4.2.7 on 2023-11-29 18:26

import django.core.validators
from django.db import migrations, models
import usuario.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_perfil_delete_perfilusuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, validators=[usuario.models.validar_fecha]),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, help_text='El numero de telefono debe ser ingresado en formato internacional', max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Formato invalido.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
