# Generated by Django 2.0.1 on 2018-06-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0012_auto_20180626_2216'),
        ('prestadores', '0010_auto_20180628_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestador',
            name='servicios',
            field=models.ManyToManyField(to='servicios.Servicio'),
        ),
    ]
