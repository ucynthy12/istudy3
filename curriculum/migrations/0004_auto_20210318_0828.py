# Generated by Django 3.1.7 on 2021-03-18 08:28

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0003_auto_20210316_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='video'),
        ),
    ]
