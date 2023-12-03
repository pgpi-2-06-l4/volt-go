import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0013_merge_20231201_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarjetacredito',
            name='cvv',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(message='El CVV debe tener 3 dígitos numéricos', regex='^\\d{3}$')]),
        ),
    ]
