# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0004_auto_20180327_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sampleselements',
            old_name='sample',
            new_name='layer',
        ),
    ]
