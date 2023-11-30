# Generated by Django 4.2.7 on 2023-11-29 20:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0010_merge_20231129_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='codigo_postal',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='El código postal debe contener 5 dígitos exactamente', regex='^\\d{5}$')]),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Formato invalido.', regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='tarjetacredito',
            name='cvv',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='El CVV debe tener 4 dígitos numéricos', regex='^\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='tarjetacredito',
            name='iban',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='El IBAN debe tener 16 dígitos numéricos', regex='^\\d{16}$')]),
        ),
    ]
