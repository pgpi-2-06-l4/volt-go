# Generated by Django 4.2.7 on 2023-12-04 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='estado_venta',
            field=models.IntegerField(choices=[(0, 'Por pagar'), (1, 'Pagado')], default=0),
        ),
    ]
