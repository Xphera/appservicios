# Generated by Django 2.0.1 on 2018-07-22 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0033_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='compraDetalle',
        ),
    ]
