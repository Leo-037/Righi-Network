# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-17 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recuperi', '0002_auto_20160914_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='gruppo',
            name='recupero',
            field=models.BooleanField(default=False),
        ),
    ]