# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0002_tutorato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorato',
            name='studente',
        ),
        migrations.RemoveField(
            model_name='tutorato',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='Tutorato',
        ),
    ]
