# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-14 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_auto_20170214_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(default='', max_length=250),
        ),
    ]
