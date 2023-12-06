# Generated by Django 4.2.7 on 2023-12-04 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField(null=True)),
                ('estado_envio', models.IntegerField(choices=[(0, 'En almacen'), (1, 'En reparto'), (2, 'Entregado')], default=0)),
                ('tipo_pago', models.IntegerField(choices=[(0, 'Contrareembolso'), (1, 'Pasarela')], default=1)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.usuario')),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
            },
        ),
        migrations.CreateModel(
            name='Reclamacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('resuelta', models.BooleanField(default=False)),
                ('venta', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.venta')),
            ],
            options={
                'verbose_name': 'reclamacion',
                'verbose_name_plural': 'reclamaciones',
            },
        ),
    ]
