# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-16 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='name',
            field=models.CharField(default='free trail', max_length=200),
        ),
    ]
