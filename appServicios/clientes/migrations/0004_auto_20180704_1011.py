# Generated by Django 2.0.1 on 2018-07-04 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_cliente_imagepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='imagePath',
            field=models.FileField(null=True, upload_to='clientes'),
        ),
    ]
