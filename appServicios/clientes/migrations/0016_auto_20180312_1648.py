# Generated by Django 2.0.1 on 2018-03-12 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0015_auto_20180302_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ubicacion',
            old_name='title',
            new_name='titulo',
        ),
    ]
