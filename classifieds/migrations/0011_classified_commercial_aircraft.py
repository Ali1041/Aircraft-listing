# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0010_auto_20180215_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='classified',
            name='commercial_aircraft',
            field=models.BooleanField(default=False),
        ),
    ]
