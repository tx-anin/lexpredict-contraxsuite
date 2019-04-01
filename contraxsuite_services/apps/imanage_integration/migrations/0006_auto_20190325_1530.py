# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-25 15:30
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imanage_integration', '0005_imanagedocument_import_problem_false'),
    ]

    operations = [
        migrations.AddField(
            model_name='imanageconfig',
            name='imanage_to_contraxsuite_field_binding',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, help_text='JSON mapping of iManage field codes to Contraxsuite \n                                                      field codes. Example: { "custom1": "field_code_1" }', null=True),
        ),
        migrations.AlterField(
            model_name='imanageconfig',
            name='assignee',
            field=models.ForeignKey(blank=True, help_text='User to which the iManage documents \n    should be assigned.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='imanageconfig',
            name='project',
            field=models.ForeignKey(blank=True, help_text='Project into which the iManage documents\n    should be saved.', null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
    ]