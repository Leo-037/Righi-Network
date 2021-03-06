# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 17:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0004_tutor_cellulare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='cellulare',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Il numero di telefono deve essere inserito in questo formato: '+999999999'.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numero di cellulare'),
        ),
    ]
