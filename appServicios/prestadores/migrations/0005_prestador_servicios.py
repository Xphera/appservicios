# Generated by Django 2.0.1 on 2018-06-28 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0012_auto_20180626_2216'),
        ('prestadores', '0004_remove_prestador_servicios'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestador',
            name='servicios',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='servicios_prestador', to='servicios.Servicio'),
        ),
    ]
