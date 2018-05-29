# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0017_irradation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='emergency_phone',
            field=models.CharField(default=63344, max_length=200),
            preserve_default=False,
        ),
    ]
