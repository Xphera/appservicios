# Generated by Django 2.0.1 on 2018-06-28 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0012_auto_20180626_2216'),
        ('prestadores', '0007_auto_20180628_1236'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrestadorSerivios',
            new_name='PrestadorSerivio',
        ),
    ]
