# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0051_experiments_public_experiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='irradiation',
            name='dos_position',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
