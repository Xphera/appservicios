# Generated by Django 2.0.1 on 2018-07-04 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestadores', '0016_auto_20180703_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formacion',
            options={'verbose_name_plural': 'Formaciones'},
        ),
        migrations.AlterField(
            model_name='prestador',
            name='imagePath',
            field=models.FileField(null=True, upload_to='prestadores'),
        ),
    ]
