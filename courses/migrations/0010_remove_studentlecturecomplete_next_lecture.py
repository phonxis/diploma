# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-26 11:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_studentlecturecomplete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentlecturecomplete',
            name='next_lecture',
        ),
    ]
