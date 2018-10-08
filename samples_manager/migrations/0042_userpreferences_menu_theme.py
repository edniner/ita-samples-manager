# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0041_auto_20181003_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='menu_theme',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
