# Generated by Django 2.0.1 on 2018-10-11 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payU', '0003_auto_20180211_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobrotarjetadecredito',
            name='confirmacion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
