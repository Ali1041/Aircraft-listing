# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-13 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0003_auto_20180213_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classified',
            name='price_usd',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]