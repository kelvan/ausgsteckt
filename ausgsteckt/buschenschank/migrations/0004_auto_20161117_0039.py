# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buschenschank', '0003_buschenschank_is_removed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buschenschank',
            options={'verbose_name': 'Buschenschank', 'verbose_name_plural': 'Buschenschänke'},
        ),
        migrations.RemoveField(
            model_name='buschenschank',
            name='activated',
        ),
        migrations.AddField(
            model_name='buschenschank',
            name='osm_type',
            field=models.CharField(blank=True, choices=[('node', 'Node'), ('way', 'Way'), ('relation', 'Relation')], max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='buschenschank',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
