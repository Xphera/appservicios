# Generated by Django 2.0.1 on 2018-07-10 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0025_auto_20180710_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comprahistorico',
            name='usuarior',
        ),
    ]
