# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-13 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0006_auto_20180213_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classified',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logos'),
        ),
    ]
