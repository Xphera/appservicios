# Generated by Django 2.0.1 on 2018-09-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0043_auto_20180828_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
