# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20170110_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('id', 'slug')]),
        ),
    ]
