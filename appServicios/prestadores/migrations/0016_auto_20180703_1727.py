# Generated by Django 2.0.1 on 2018-07-03 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prestadores', '0015_auto_20180703_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestadorpaquete',
            name='prestador',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prestador_paquetes', to='prestadores.Prestador'),
        ),
    ]
