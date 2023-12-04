# Generated by Django 4.2.7 on 2023-12-04 20:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_remove_itemcarrito_venta'),
        ('tienda', '0003_alter_venta_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
                ('venta', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.venta')),
            ],
            options={
                'verbose_name': 'item_venta',
                'verbose_name_plural': 'items_venta',
            },
        ),
    ]
