# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0019_auto_20180607_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='db_telephone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='department',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='group',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='home_institute',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
