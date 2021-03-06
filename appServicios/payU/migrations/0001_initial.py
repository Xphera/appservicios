# Generated by Django 2.0.1 on 2018-04-19 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CobroTarjetaDeCredito',
            fields=[
                ('referenceCode', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('notifyUrl', models.CharField(blank=True, max_length=100, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('cuotas', models.IntegerField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('orderId', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('responseCode', models.CharField(blank=True, max_length=60, null=True)),
                ('trnsancion', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente')),
            ],
            options={
                'verbose_name_plural': 'cobrosTarjetaDeCredito',
            },
        ),
        migrations.CreateModel(
            name='CodigoRespuetaPayu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=60)),
                ('descripcion', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TarjetaDeCredito',
            fields=[
                ('creditCardTokenId', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('identificationNumber', models.IntegerField(blank=True, null=True)),
                ('paymentMethod', models.CharField(max_length=10)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('expirationDate', models.DateField(blank=True, null=True)),
                ('creationDate', models.CharField(blank=True, max_length=50, null=True)),
                ('maskedNumber', models.CharField(blank=True, max_length=50, null=True)),
                ('principal', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('payerId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente')),
            ],
            options={
                'verbose_name_plural': 'tarjetasDeCredito',
            },
        ),
    ]
