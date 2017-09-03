# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170903_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='origin',
            field=models.ImageField(upload_to='p_img/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='webp',
            field=models.ImageField(blank=True, null=True, upload_to='p_img/%Y/%m/%d/'),
        ),
    ]