# Generated by Django 2.0.1 on 2018-03-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestadores', '0005_auto_20180302_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestador',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]