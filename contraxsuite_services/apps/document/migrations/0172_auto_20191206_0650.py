# Generated by Django 2.2.4 on 2019-12-06 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0171_migrate_textunit_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textunit',
            name='text',
        ),
        migrations.AlterField(
            model_name='textunittext',
            name='text',
            field=models.TextField(max_length=16384, null=True),
        ),
    ]