# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 06:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripPlanner', '0004_auto_20170617_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='question',
        ),
    ]