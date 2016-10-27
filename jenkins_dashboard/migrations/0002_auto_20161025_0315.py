# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 03:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jenkins_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jenkinsresults',
            old_name='fail_number',
            new_name='fail_numbers',
        ),
        migrations.RenameField(
            model_name='jenkinsresults',
            old_name='pass_number',
            new_name='pass_numbers',
        ),
        migrations.RenameField(
            model_name='jenkinstestcase',
            old_name='action',
            new_name='total_actions',
        ),
        migrations.RenameField(
            model_name='jenkinstestcase',
            old_name='condition',
            new_name='total_conditions',
        ),
    ]