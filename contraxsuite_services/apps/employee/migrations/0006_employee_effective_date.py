# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_remove_employee_effective_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='effective_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
