# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-19 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0014_auto_20180219_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aircraftmake',
            options={'ordering': ['-number_of_classifieds']},
        ),
        migrations.AddField(
            model_name='aircraftmake',
            name='number_of_classifieds',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
