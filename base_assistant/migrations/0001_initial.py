# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VersionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=20)),
                ('platform_ver', models.CharField(max_length=20)),
                ('product_ver', models.CharField(max_length=20)),
                ('verinfo', models.CharField(max_length=200)),
            ],
        ),
    ]