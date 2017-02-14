# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-14 09:01
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0017_quiz_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='module',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='order',
        ),
        migrations.AddField(
            model_name='question',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 2, 14, 9, 0, 31, 97417, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='question_related', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 2, 14, 9, 0, 45, 724254, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 2, 14, 9, 0, 52, 39615, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='data_field',
            field=models.TextField(default='question', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_related', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 2, 14, 9, 1, 15, 590962, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
