# Generated by Django 2.0.1 on 2018-08-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_cliente_estadousuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='estadoUsuario',
        ),
        migrations.AddField(
            model_name='cliente',
            name='cerrarCuenta',
            field=models.BooleanField(default=False),
        ),
    ]
