# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 14:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permit', '0008_auto_20160108_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business_profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]