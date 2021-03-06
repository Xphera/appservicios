# Generated by Django 2.0.1 on 2018-04-19 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientes', '0001_initial'),
        ('servicios', '0001_initial'),
        ('parametrizacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='servicios.Compra'),
        ),
        migrations.AddField(
            model_name='sesion',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametrizacion.EstadoSesion'),
        ),
        migrations.AddField(
            model_name='sesion',
            name='ubicacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Ubicacion'),
        ),
        migrations.AddField(
            model_name='mediodepago',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medio_de_pago', to='clientes.Cliente'),
        ),
        migrations.AddField(
            model_name='mediodepago',
            name='franquicia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medio_de_pago', to='parametrizacion.FranquiciasTarjetasCredito'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='sexo',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='parametrizacion.Sexo'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='clientes', to=settings.AUTH_USER_MODEL),
        ),
    ]
