# Generated by Django 4.2.7 on 2023-12-07 12:26

from django.db import migrations, models
import usuario.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_alter_perfil_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='calle',
            field=models.CharField(max_length=100, validators=[usuario.models.validate_letters]),
        ),
        migrations.DeleteModel(
            name='TarjetaCredito',
        ),
    ]