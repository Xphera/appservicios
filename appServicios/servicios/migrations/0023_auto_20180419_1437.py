# Generated by Django 2.0.1 on 2018-04-19 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0022_compradetalle_duracionsesion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compradetallesesion',
            options={'ordering': ('fechaInicio',), 'verbose_name_plural': 'CompraDetallesSesiones'},
        ),
    ]
