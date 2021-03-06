# Generated by Django 2.0.1 on 2018-07-03 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prestadores', '0013_auto_20180628_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('institucion', models.CharField(max_length=100, verbose_name='Institucion')),
                ('año', models.IntegerField(verbose_name='Año')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('prestador', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prestador_formacion', to='prestadores.Prestador')),
            ],
        ),
        migrations.RemoveField(
            model_name='estudio',
            name='prestador',
        ),
        migrations.DeleteModel(
            name='Estudio',
        ),
    ]
