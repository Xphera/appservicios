# Generated by Django 2.0.1 on 2018-07-22 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servicios', '0035_auto_20180722_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('compraDetalleSesion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compraDetalleSesionesChat', to='servicios.CompraDetalleSesion')),
                ('usuario', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='chatUsuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]