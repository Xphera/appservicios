# Generated by Django 2.0.1 on 2018-04-01 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compradetalle',
            name='compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compraDetallesxxx', to='servicios.Compra'),
        ),
    ]