# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-19 09:00
from __future__ import unicode_literals

import courses.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170114_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('order', courses.fields.OrderField(blank=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='courses.Module')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='content',
            name='module',
        ),
        migrations.AddField(
            model_name='content',
            name='lecture',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='courses.Lecture'),
            preserve_default=False,
        ),
    ]