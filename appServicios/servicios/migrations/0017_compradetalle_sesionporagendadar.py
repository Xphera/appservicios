# Generated by Django 2.0.1 on 2018-04-09 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0016_auto_20180409_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='compradetalle',
            name='sesionPorAgendadar',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]