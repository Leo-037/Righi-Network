# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recuperi', '0003_gruppo_recupero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giorno',
            name='nome',
            field=models.CharField(max_length=9, verbose_name='Giorno'),
        ),
    ]
