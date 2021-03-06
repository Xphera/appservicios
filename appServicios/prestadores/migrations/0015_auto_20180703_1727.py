# Generated by Django 2.0.1 on 2018-07-03 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0012_auto_20180626_2216'),
        ('prestadores', '0014_auto_20180703_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrestadorPaquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('paquete', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paquetes_prestador', to='servicios.Paquete')),
                ('prestador', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prestador_servicio', to='prestadores.Prestador')),
            ],
        ),
        migrations.RemoveField(
            model_name='prestadorservicio',
            name='prestador',
        ),
        migrations.RemoveField(
            model_name='prestadorservicio',
            name='servicios',
        ),
        migrations.DeleteModel(
            name='PrestadorServicio',
        ),
    ]
