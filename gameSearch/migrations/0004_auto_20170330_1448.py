# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-30 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameSearch', '0003_auto_20170330_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourites',
            name='user',
            field=models.IntegerField(max_length=11),
        ),
    ]