# Generated by Django 2.0.1 on 2018-08-28 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0012_auto_20180828_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='cerrarCuenta',
            new_name='cuentaCerrada',
        ),
    ]
