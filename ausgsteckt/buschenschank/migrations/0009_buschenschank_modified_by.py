# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buschenschank', '0008_auto_20170101_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='buschenschank',
            name='modified_by',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Last edit OSM user'),
        ),
    ]
