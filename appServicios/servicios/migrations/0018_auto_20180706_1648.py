# Generated by Django 2.0.1 on 2018-07-06 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0017_auto_20180706_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compradetallesesion',
            name='latitud',
            field=models.DecimalField(blank=True, decimal_places=16, max_digits=21, null=True),
        ),
        migrations.AlterField(
            model_name='compradetallesesion',
            name='longitud',
            field=models.DecimalField(blank=True, decimal_places=16, max_digits=21, null=True),
        ),
    ]
