# Generated by Django 2.0.1 on 2018-04-09 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0015_auto_20180409_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compradetalle',
            name='sesionAgendadas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='compradetalle',
            name='sesionFinalizadas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]