# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-02 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0079_documenttypefield_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfield',
            options={'ordering': ('code',)},
        ),
        migrations.RemoveField(
            model_name='documentfield',
            name='order',
        ),
    ]
