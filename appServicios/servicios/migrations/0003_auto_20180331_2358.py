# Generated by Django 2.0.1 on 2018-04-01 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_auto_20180331_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compradetalle',
            name='compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compraDetalles', to='servicios.Compra'),
        ),
    ]