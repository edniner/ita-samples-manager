# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0018_experiments_emergency_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='irradation',
            old_name='position',
            new_name='table_position',
        ),
        migrations.AddField(
            model_name='irradation',
            name='irrad_table',
            field=models.CharField(default='IRRAD', max_length=50),
            preserve_default=False,
        ),
    ]
