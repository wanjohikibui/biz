# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 17:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permit', '0007_auto_20160108_1318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='county',
            options={'verbose_name_plural': 'Bungoma County'},
        ),
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name_plural': 'Bungoma Locations'},
        ),
    ]
