# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-29 16:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_assistant', '0004_wikiinfo_contetn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wikiinfo',
            old_name='contetn',
            new_name='content',
        ),
    ]