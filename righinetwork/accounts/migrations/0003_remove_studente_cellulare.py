# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 16:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_studente_cellulare'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studente',
            name='cellulare',
        ),
    ]