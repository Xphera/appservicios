# Generated by Django 2.0.1 on 2018-07-10 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0027_comprahistorico_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compradetallesesionhistorico',
            old_name='nombreCompleto',
            new_name='usuarioNombreCompleto',
        ),
        migrations.AddField(
            model_name='compradetallesesionhistorico',
            name='estadoNombre',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
