# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-09 03:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_assistant', '0004_auto_20170909_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='next_solution',
            field=models.ManyToManyField(to='base_assistant.Solution', verbose_name='子解决方法'),
        ),
    ]
