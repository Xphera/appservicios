# Generated by Django 2.0.1 on 2018-02-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0007_cliente_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ubicacion',
            name='imgPath',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='latitud',
            field=models.DecimalField(decimal_places=16, max_digits=21),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='longitud',
            field=models.DecimalField(decimal_places=16, max_digits=21),
        ),
    ]