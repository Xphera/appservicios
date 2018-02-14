# Generated by Django 2.0.1 on 2018-02-12 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0002_auto_20180205_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='imagePath',
            field=models.FileField(upload_to='media/categorias'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compras', to='clientes.Cliente'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='paquete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compras', to='servicios.Paquete'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='prestador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paquetes', to='prestadores.Prestador'),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='paquetes', to='servicios.Servicio'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicios', to='servicios.Categoria', verbose_name='Categoria del servicio'),
        ),
    ]