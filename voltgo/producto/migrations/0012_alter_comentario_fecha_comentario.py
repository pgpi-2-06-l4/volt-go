
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0011_merge_0008_comentario_0010_alter_producto_precio_base'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha_comentario',
            field=models.DateField(auto_now=True),
        ),
    ]
