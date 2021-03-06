# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0128_auto_20190409_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='code',
            field=models.CharField(db_index=True, help_text='Field codes are used for creating \n    columns in DB tables, in field formulas (Python syntax), for human-readable data representation in APIs. \n    Field codes must be lowercase, should start with a latin letter and contain only latin letters, digits, \n    and underscores. You cannot use a field code you have already used for this document type.', max_length=50),
        ),
    ]
