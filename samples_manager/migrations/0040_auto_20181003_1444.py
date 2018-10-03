# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0039_auto_20181003_1435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreferences',
            old_name='theme',
            new_name='global_theme',
        ),
    ]
