# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 14:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170903_1624'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='preview',
            new_name='webp',
        ),
    ]
