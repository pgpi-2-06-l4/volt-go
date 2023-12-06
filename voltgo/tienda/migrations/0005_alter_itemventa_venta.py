# Generated by Django 4.2.7 on 2023-12-05 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0004_itemventa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemventa',
            name='venta',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tienda.venta'),
        ),
    ]
