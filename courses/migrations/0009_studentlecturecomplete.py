# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-25 16:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0008_auto_20170119_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentLectureComplete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('date_completed', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_completed_lecture', to='courses.Lecture')),
                ('next_lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_next_lecture', to='courses.Lecture')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
