# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-12 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameSearch', '0006_auto_20170330_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourites',
            name='game',
            field=models.CharField(max_length=5),
        ),
    ]
