# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0042_userpreferences_menu_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='table_theme',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
