# Generated by Django 4.2.7 on 2023-12-01 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_alter_tarjetacredito_cvv'),
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclamacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('resuelta', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.usuario')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.venta')),
            ],
            options={
                'verbose_name': 'reclamacion',
                'verbose_name_plural': 'reclamaciones',
            },
        ),
    ]