# Generated by Django 2.0.1 on 2018-07-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_auto_20180704_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='saldoBolsa',
            field=models.FloatField(default=0),
        ),
    ]
