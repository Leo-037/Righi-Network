# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('tutoring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Studente')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoring.Tutor')),
            ],
        ),
    ]