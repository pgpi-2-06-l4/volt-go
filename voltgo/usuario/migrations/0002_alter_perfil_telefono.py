# Generated by Django 4.2.7 on 2023-12-06 10:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='Formato invalido.', regex='^(\\+34|0034|34)?[6789]\\d{8}$')]),
        ),
    ]
