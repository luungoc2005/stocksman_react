# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0009_dailyprice_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyprice',
            name='industry',
        ),
        migrations.AddField(
            model_name='stock',
            name='industry',
            field=models.IntegerField(default=0),
        ),
    ]