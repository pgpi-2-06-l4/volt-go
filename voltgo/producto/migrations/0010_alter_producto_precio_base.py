# Generated by Django 4.2.7 on 2023-12-02 11:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0009_alter_caracteristica_valor_alter_producto_empresa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio_base',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
