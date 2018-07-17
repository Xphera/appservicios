# Generated by Django 2.0.1 on 2018-07-11 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametrizacion', '0001_initial'),
        ('servicios', '0030_auto_20180710_1453'),
        ('clientes', '0005_cliente_saldobolsa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bolsa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=10)),
                ('descripcion', models.TextField()),
                ('valor', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente')),
                ('compraDetalle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bolsaCompraDetalle', to='servicios.CompraDetalle')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametrizacion.EstadoSesion')),
            ],
        ),
    ]